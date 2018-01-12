from pathlib import Path

import minicli
import requests
from usine import (cd, chown, config, cp, enter, env, exists, exit, mkdir, put,
                   run, screen, sudo)


def put_dir(local, remote):
    local = Path(local)
    remote = Path(remote)
    for path in local.rglob('*'):
        relative_path = path.relative_to(local)
        if path.is_dir():
            with sudo(user='tilery'):
                mkdir(remote / relative_path)
        else:
            put(str(path), str(remote / relative_path))


def python(cmd):
    with sudo(user='tilery'):
        run(f'/srv/tilery/venv/bin/python {cmd}')


@minicli.cli
def pip(cmd):
    with sudo(user='tilery'):
        run(f'/srv/tilery/venv/bin/pip {cmd}')


@minicli.cli
def system():
    with sudo():
        run('apt update')
        run('apt install -y postgresql-9.5 postgresql-9.5-postgis-2.2 '
            'software-properties-common wget nginx unzip autoconf libtool g++ '
            'apache2 apache2-dev libmapnik-dev libleveldb1v5 libgeos-dev '
            'libprotobuf-dev unifont curl zlib1g-dev uuid-dev python-psycopg2')
        # Prevent conflict with nginx.
        run('apt install -y apache2 apache2-dev')
        run('useradd -N tilery -d /srv/tilery/ || exit 0')
        mkdir('/srv/tilery/src')
        mkdir('/srv/tilery/tmp')
        mkdir('/srv/tilery/letsencrypt/.well-known/acme-challenge')
        chown('tilery:users', '/srv/tilery/')
        run('chsh -s /bin/bash tilery')
    install_imposm3()
    install_mod_tile()
    configure_mod_tile()
    install_netdata()


def install_netdata(force=False):
    if not exists('/etc/systemd/system/netdata.service') or force:
        run('bash <(curl -Ss https://my-netdata.io/kickstart.sh) --dont-wait')
    put('scripts/netdata.conf', '/etc/netdata/netdata.conf')
    restart(services='netdata')


def install_imposm3(force=False):
    if exists('/usr/bin/imposm3') and not force:
        print('imposm3 already installed')
        return
    run('wget https://imposm.org/static/rel/imposm3-0.4.0dev-20170519-3f00374-linux-x86-64.tar.gz -O /tmp/imposm3.tar.gz')  # noqa
    run('tar -xzf /tmp/imposm3.tar.gz --directory /tmp')
    with sudo():
        cp('/tmp/imposm3-0.4.0dev-20170519-3f00374-linux-x86-64/imposm3',
           '/usr/bin/imposm3')
    with sudo(user='tilery'):
        mkdir('/srv/tilery/tmp/imposm')


def install_mod_tile(force=False):
    if exists('/usr/local/bin/renderd') and not force:
        print('mod_tile already installed')
        return
    run('wget https://github.com/SomeoneElseOSM/mod_tile/archive/master.zip -O /tmp/mod_tile.zip')  # noqa
    run('unzip -n /tmp/mod_tile.zip -d /tmp/')
    with cd('/tmp/mod_tile-master'):
        run('./autogen.sh')
        run('./configure')
        run('make')
        with sudo():
            run('make install')
            run('make install-mod_tile')
            run('ldconfig')
    with sudo(user='tilery'):
        mkdir('/var/run/renderd')


def configure_mod_tile():
    with sudo(user='tilery'):
        mkdir('/srv/tilery/tmp/tiles')
        mkdir('/srv/tilery/renderd')
    with sudo(), cd('/etc/apache2/'):
        put('scripts/tile.load', 'mods-available/tile.load')
        put('scripts/tile.conf', 'mods-available/tile.conf')
        put('scripts/apache.conf', 'sites-enabled/000-default.conf')
        put('scripts/ports.conf', 'ports.conf')
        run('a2enmod tile')


@minicli.cli
def db():
    with sudo(user='postgres'):
        run('createuser tilery || exit 0')
        run('createdb tilery -O tilery || exit 0')
        run('psql tilery -c "CREATE EXTENSION IF NOT EXISTS postgis"')


@minicli.cli
def http():
    # When we'll have a domain.
    # put('scripts/letsencrypt.conf', '/etc/nginx/snippets/letsencrypt.conf')
    # put('scripts/ssl.conf', '/etc/nginx/snippets/ssl.conf')
    if exists('/etc/letsencrypt/live/drone.api.gouv.fr/fullchain.pem'):
        conf = 'scripts/nginx-https.conf'
    else:
        # Before letsencrypt.
        conf = 'scripts/nginx-http.conf'
    put(conf, '/etc/nginx/sites-enabled/default')
    restart()


@minicli.cli
def bootstrap():
    system()
    db()
    services()
    http()
    # letsencrypt()
    # Now put the https ready Nginx conf.
    # http()
    ssh_keys()


@minicli.cli
def letsencrypt():
    with sudo():
        run('add-apt-repository ppa:certbot/certbot')
        run('apt update')
        run('apt install -y certbot')
    put('scripts/certbot.ini', '/srv/tilery/certbot.ini')
    put('scripts/ssl-renew', '/etc/cron.weekly/ssl-renew')
    run('chmod +x /etc/cron.weekly/ssl-renew')
    run('certbot certonly -c /srv/tilery/certbot.ini --non-interactive '
        '--agree-tos')


@minicli.cli
def services():
    service('renderd')
    service('imposm')


def service(name):
    put(f'scripts/{name}.service /etc/systemd/system/{name}.service')
    run(f'systemctl enable {name}.service')


@minicli.cli
def ssh_keys():
    with sudo():
        for name, url in config.get('ssh_key_urls', {}).items():
            key = requests.get(url).text.replace('\n', '')
            run('grep -q -r "{key}" .ssh/authorized_keys || echo "{key}" '
                '| tee --append .ssh/authorized_keys'.format(key=key))


@minicli.cli
def deploy():
    put('mapping.yml', '/srv/tilery/mapping.yml')
    put('scripts/imposm.conf', '/srv/tilery/imposm.conf')
    put('scripts/renderd.conf', '/srv/tilery/renderd.conf')
    put('scripts/index.html', '/srv/tilery/index.html')


def download_shapefile(name, url, force):
    datapath = '/srv/tilery/data/'
    if not exists(datapath + name) or force:
        run(f'wget {url} -O /tmp/data.zip --quiet')
        run(f'unzip -n /tmp/data.zip -d {datapath}')


@minicli.cli
def download(force=False):
    path = '/srv/tilery/tmp/planet-latest.osm.pbf'
    if not exists(path) or force:
        run('wget https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf'
            f' -O {path} --quiet')
    domain = 'http://data.openstreetmapdata.com/'
    download_shapefile(
        'simplified-land-polygons-complete-3857/simplified_land_polygons.shp',
        f'{domain}simplified-land-polygons-complete-3857.zip', force)
    download_shapefile('land-polygons-split-3857/land_polygons.shp',
                       f'{domain}land-polygons-split-3857.zip', force)
    domain = 'http://nuage.yohanboniface.me/'
    download_shapefile('boundary_lines/boundary_lines_simplified.shp',
                       f'{domain}boundary_lines_simplified.zip', force)
    download_shapefile('boundary_lines_simplified/boundary_lines.shp',
                       f'{domain}boundary_lines.zip', force)


@minicli.cli(name='import')
def import_data(remove_backup=False):
    with sudo(user='tilery'), env(PGHOST='/var/run/postgresql/'), screen():
        if remove_backup:
            run('imposm3 import -config /srv/tilery/imposm.conf -removebackup')
        run('imposm3 import -diff -config /srv/tilery/imposm.conf '
            '-read /srv/tilery/tmp/planet-latest.osm.pbf -appendcache')
        run('imposm3 import -config /srv/tilery/imposm.conf -diff -write '
            '-deployproduction')


@minicli.cli
def systemctl(cmd):
    run(f'systemctl {cmd}')


@minicli.cli
def logs(lines=50, services=None):
    if not services:
        services = 'renderd apache2 nginx imposm'
    services = ' --unit '.join(services.split())
    run(f'journalctl --lines {lines} --unit {services}')


@minicli.cli
def psql(query):
    with sudo(user='postgres'):
        run(f'psql tilery -c "{query}"')


@minicli.cli
def clear_cache():
    run('rm -rf /srv/tilery/tmp/tiles/*')


@minicli.cli
def restart(services=None):
    services = services or 'renderd apache2 nginx imposm'
    run('sudo systemctl restart {}'.format(services))


@minicli.cli
def render(map='default', min=1, max=10):
    with sudo(user='tilery'):
        run(f'render_list --map {map} --all --force --num-threads 8 '
            f'--socket /var/run/renderd/renderd.sock '
            f'--tile-dir /srv/tilery/tmp/tiles '
            f' --min-zoom {min} --max-zoom {max}')


@minicli.cli
def boundary(force=False):
    if not exists('/tmp/boundary.sql') or force:
        put('tmp/boundary.sql', '/tmp/boundary.sql')
    with sudo(user='tilery'):
        run('psql --single-transaction -d tilery --file /tmp/boundary.sql')


@minicli.before
def before(hostname):
    enter(hostname=hostname)


@minicli.after
def after():
    exit()


if __name__ == '__main__':
    minicli.run(hostname='pianoforte')
