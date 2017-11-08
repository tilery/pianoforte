from hashlib import md5
from pathlib import Path

from invoke import task
import requests


def as_user(ctx, user, cmd, *args, **kwargs):
    ctx.run('sudo --set-home --preserve-env --user {} --login '
            '{}'.format(user, cmd), *args, **kwargs)


def as_tilery(ctx, cmd, *args, **kwargs):
    as_user(ctx, 'tilery', cmd)


def as_postgres(ctx, cmd, *args, **kwargs):
    as_user(ctx, 'postgres', cmd)


def sudo_put(ctx, local, remote, chown=None):
    tmp = str(Path('/tmp') / md5(remote.encode()).hexdigest())
    ctx.put(local, tmp)
    ctx.run('sudo mv {} {}'.format(tmp, remote))
    if chown:
        ctx.run('sudo chown {} {}'.format(chown, remote))


def put_dir(ctx, local, remote):
    local = Path(local)
    remote = Path(remote)
    for path in local.rglob('*'):
        relative_path = path.relative_to(local)
        if path.is_dir():
            as_tilery(ctx, 'mkdir -p {}'.format(remote / relative_path))
        else:
            sudo_put(ctx, str(path), str(remote / relative_path))


def python(ctx, command):
    as_tilery(ctx, '/srv/tilery/venv/bin/python {}'.format(command))


@task
def pip(ctx, command):
    as_tilery(ctx, '/srv/tilery/venv/bin/pip {}'.format(command))


@task
def system(ctx):
    ctx.run('sudo apt update')
    ctx.run('sudo apt install -y postgresql-9.5 postgresql-9.5-postgis-2.2 '
            'software-properties-common wget nginx unzip autoconf libtool g++ '
            'apache2 apache2-dev libmapnik-dev libleveldb1v5 libgeos-dev '
            'libprotobuf-dev')
    # Prevent conflict with nginx.
    ctx.run('sudo apt install -y apache2 apache2-dev')
    ctx.run('sudo mkdir -p /srv/tilery/src')
    ctx.run('sudo mkdir -p /srv/tilery/tmp')
    ctx.run('sudo mkdir -p /srv/tilery/letsencrypt/.well-known/acme-challenge')
    ctx.run('sudo useradd -N tilery -d /srv/tilery/ || exit 0')
    ctx.run('sudo chown tilery:users /srv/tilery/')
    ctx.run('sudo chown tilery:users /srv/tilery/src/')
    ctx.run('sudo chsh -s /bin/bash tilery')
    install_imposm3(ctx)
    install_mod_tile(ctx)
    configure_mod_tile(ctx)


def install_imposm3(ctx, force=False):
    exists = ctx.run('if [ -f "/usr/bin/imposm3" ]; then echo 1; fi')
    if not exists.stdout or force:
        ctx.run('sudo wget https://imposm.org/static/rel/imposm3-0.4.0dev-20170519-3f00374-linux-x86-64.tar.gz -O /tmp/imposm3.tar.gz')  # noqa
        ctx.run('sudo tar -xzf /tmp/imposm3.tar.gz --directory /tmp')
        ctx.run('sudo cp /tmp/imposm3-0.4.0dev-20170519-3f00374-linux-x86-64/imposm3 /usr/bin/imposm3')  # noqa
    else:
        print('imposm3 already installed')


def install_mod_tile(ctx, force=False):
    exists = ctx.run('if [ -f "/usr/local/bin/renderd" ]; then echo 1; fi')
    if not exists.stdout or force:
        ctx.run('wget https://github.com/SomeoneElseOSM/mod_tile/archive/master.zip -O /tmp/mod_tile.zip')  # noqa
        ctx.run('unzip -n /tmp/mod_tile.zip -d /tmp/')
        ctx.run('cd /tmp/mod_tile-master && ./autogen.sh')
        ctx.run('cd /tmp/mod_tile-master && ./configure')
        ctx.run('cd /tmp/mod_tile-master && make')
        ctx.run('cd /tmp/mod_tile-master && sudo make install')
        ctx.run('cd /tmp/mod_tile-master && sudo make install-mod_tile')
        ctx.run('cd /tmp/mod_tile-master && sudo ldconfig')
        ctx.run('sudo mkdir -p /var/run/renderd')
        ctx.run('sudo chown tilery:users /var/run/renderd')
    else:
        print('mod_tile already installed')


def configure_mod_tile(ctx):
    ctx.run('sudo mkdir -p /srv/tilery/cache')
    ctx.run('sudo chown tilery:users /srv/tilery/cache')
    ctx.run('sudo mkdir -p /srv/tilery/renderd')
    ctx.run('sudo chown tilery:users /srv/tilery/renderd')
    sudo_put(ctx, 'fabfile/tile.load', '/etc/apache2/mods-available/tile.load')
    sudo_put(ctx, 'fabfile/tile.conf', '/etc/apache2/mods-available/tile.conf')
    sudo_put(ctx, 'fabfile/apache.conf',
             '/etc/apache2/sites-enabled/000-default.conf')
    sudo_put(ctx, 'fabfile/ports.conf', '/etc/apache2/ports.conf')
    ctx.run('sudo a2enmod tile')


@task
def db(ctx):
    as_postgres(ctx, 'createuser tilery || exit 0')
    as_postgres(ctx, 'createdb tilery -O tilery || exit 0')
    as_postgres(ctx, 'psql tilery -c "CREATE EXTENSION IF NOT EXISTS postgis"')


@task
def http(ctx):
    # When we'll have a domain.
    # sudo_put(ctx, 'fabfile/letsencrypt.conf',
    #          '/etc/nginx/snippets/letsencrypt.conf')
    # sudo_put(ctx, 'fabfile/ssl.conf', '/etc/nginx/snippets/ssl.conf')
    certif = "/etc/letsencrypt/live/drone.api.gouv.fr/fullchain.pem"
    exists = ctx.run('if [ -f "{}" ]; then echo 1; fi'.format(certif))
    if exists.stdout:
        conf = 'fabfile/nginx-https.conf'
    else:
        # Before letsencrypt.
        conf = 'fabfile/nginx-http.conf'
    sudo_put(ctx, conf, '/etc/nginx/sites-enabled/default')
    restart(ctx)


@task
def bootstrap(ctx):
    system(ctx)
    db(ctx)
    services(ctx)
    http(ctx)
    # letsencrypt(ctx)
    # Now put the https ready Nginx conf.
    # http(ctx)
    ssh_keys(ctx)


@task
def letsencrypt(ctx):
    ctx.run('sudo add-apt-repository ppa:certbot/certbot')
    ctx.run('sudo apt update')
    ctx.run('sudo apt install -y certbot')
    sudo_put(ctx, 'fabfile/certbot.ini', '/srv/tilery/certbot.ini')
    sudo_put(ctx, 'fabfile/ssl-renew', '/etc/cron.weekly/ssl-renew')
    ctx.run('chmod +x /etc/cron.weekly/ssl-renew')
    ctx.run('certbot certonly -c /srv/tilery/certbot.ini --non-interactive '
            '--agree-tos')


@task
def services(ctx):
    service(ctx, 'renderd')


def service(ctx, name):
    sudo_put(ctx, 'fabfile/{}.service'.format(name),
             '/etc/systemd/system/{}.service'.format(name))
    ctx.run('systemctl enable {}.service'.format(name))


@task
def ssh_keys(ctx):
    for name, url in ctx.config.get('ssh_key_urls', {}).items():
        key = requests.get(url).text.replace('\n', '')
        ctx.run('grep -q -r "{key}" .ssh/authorized_keys '
                '|| echo "{key}" '
                '| sudo tee --append .ssh/authorized_keys'.format(key=key))


@task
def deploy(ctx):
    sudo_put(ctx, 'mapping.yml', '/srv/tilery/mapping.yml')
    sudo_put(ctx, 'fabfile/renderd.conf', '/srv/tilery/renderd.conf')
    sudo_put(ctx, 'fabfile/index.html', '/srv/tilery/index.html')


@task
def download(ctx, force=False):
    path = '/srv/tilery/tmp/lebanon-latest.osm.pbf'
    exists = ctx.run(f'if [ -f "{path}" ]; then echo 1; fi')
    if not exists.stdout or force:
        ctx.run('wget http://download.geofabrik.de/asia/lebanon-latest.osm.pbf'
                f' -O {path} --quiet')
    path = '/srv/tilery/tmp/france-latest.osm.pbf'
    exists = ctx.run(f'if [ -f "{path}" ]; then echo 1; fi')
    if not exists.stdout or force:
        ctx.run('wget '
                'http://download.geofabrik.de/europe/france-latest.osm.pbf'
                f' -O {path} --quiet')
    datapath = '/srv/tilery/data'
    domain = 'http://data.openstreetmapdata.com/'
    exists = ctx.run(f'if [ -f "{datapath}/simplified_land_polygons.shp" ]; '
                     'then echo 1; fi')
    if not exists.stdout or force:
        ctx.run(f'wget {domain}simplified-land-polygons-complete-3857.zip'
                f' -O /tmp/land-low.zip --quiet')
        ctx.run(f'unzip -n /tmp/land-low.zip -d {datapath}')
    exists = ctx.run(f'if [ -f "{datapath}/land_polygons.shp" ]; '
                     'then echo 1; fi')
    if not exists.stdout or force:
        ctx.run(f'wget {domain}land-polygons-split-3857.zip -O /tmp/land.zip '
                '--quiet')
        ctx.run(f'unzip -n /tmp/land.zip -d {datapath}')


@task
def import_data(ctx):
    as_tilery(ctx,
              'env PGHOST=/var/run/postgresql/ imposm3 import '
              '-mapping /srv/tilery/mapping.yml '
              '-read /srv/tilery/tmp/france-latest.osm.pbf '
              '-connection="postgis:///tilery" -overwritecache')
    as_tilery(ctx,
              'env PGHOST=/var/run/postgresql/ imposm3 import '
              '-mapping /srv/tilery/mapping.yml '
              '-read /srv/tilery/tmp/lebanon-latest.osm.pbf '
              '-connection="postgis:///tilery" -appendcache')
    as_tilery(ctx,
              'env PGHOST=/var/run/postgresql/ imposm3 import '
              '-mapping /srv/tilery/mapping.yml '
              '-connection="postgis:///tilery" -write '
              '-deployproduction')


@task
def systemctl(ctx, cmd):
    ctx.run('systemctl {}'.format(cmd))


@task
def logs(ctx, lines=50):
    ctx.run(f'journalctl --lines {lines} --unit renderd --unit apache2 '
            '--unit nginx')


@task
def psql(ctx, query, dbname='wolf'):
    as_postgres(ctx, f'psql tilery -c "{query}"')


@task
def clear_cache(ctx):
    ctx.run('rm -rf /srv/tilery/cache/*')


@task
def restart(ctx, services=None):
    services = services or 'renderd apache2 nginx'
    ctx.run('sudo systemctl restart {}'.format(services))
