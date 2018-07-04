import minicli
from usine import config, exists, mkdir, put, run, sudo, template

from ..commons import append_line, main, restart, ssh_keys, systemctl


@minicli.cli
def system():
    """Install the host system deps."""
    # Not installed in minimized 18.04.
    run('which sudo || apt install sudo')
    with sudo():
        run('apt update')
        run('apt install -y nginx lxc')
        mkdir('/data')  # LXC rootfs. Should be created by the partionning.


def lxc_bootstrap():
    put('remote/host/lxc-net', '/etc/default/lxc-net')
    put('remote/host/dnsmasq-hosts.conf', '/etc/lxc/dnsmasq-hosts.conf')
    put('remote/host/dnsmasq.conf', '/etc/lxc/dnsmasq.conf')
    restart('lxc-net')


@minicli.cli
def lxc_create(name):
    """Install and configure an LXC container."""
    if name not in run('lxc-ls'):
        mkdir(f'/data/lxc/{name}')
        mkdir(f'/data/lxc/{name}/ssd/')
        mkdir(f'/ssd/{name}')
        run(f'lxc-create --name {name} --dir /data/lxc/{name} '
            f'--template download -- -d ubuntu -r bionic -a amd64')
        append_line(f'/var/lib/lxc/{name}/config',
                    f'lxc.apparmor.allow_incomplete = 1')
        append_line(f'/var/lib/lxc/{name}/config',
                    f'lxc.mount.entry = /ssd/{name} ssd none bind 0 0')
        run(f'lxc-start -n {name}')
    run(f'lxc-attach -n {name} -- apt install -y openssh-server')
    mkdir(f'/data/lxc/{name}/root/.ssh/')
    run(f'cp /root/.ssh/authorized_keys* '
        f'/data/lxc/{name}/root/.ssh/authorized_keys')
    put('remote/host/lxc-resolv.conf',
        f'/data/lxc/{name}/etc/resolv.conf')


@minicli.cli
def http():
    """Configure Nginx and letsencrypt."""
    # When we'll have a domain.
    put('remote/host/piano.conf', '/etc/nginx/snippets/piano.conf')
    put('remote/host/forte.conf', '/etc/nginx/snippets/forte.conf')
    put('remote/host/letsencrypt.conf', '/etc/nginx/snippets/letsencrypt.conf')
    put('remote/host/ssl.conf', '/etc/nginx/snippets/ssl.conf')
    domain = config.piano_domains[0]
    pempath = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
    if exists(pempath):
        print(f'{pempath} found, using https configuration')
        conf = template('remote/host/nginx-https.conf',
                        piano_domains=' '.join(config.piano_domains),
                        forte_domains=' '.join(config.forte_domains),
                        domain=domain)
    else:
        print(f'{pempath} not found, using http configuration')
        # Before letsencrypt.
        conf = template('remote/host/nginx-http.conf',
                        piano_domains=' '.join(config.piano_domains),
                        forte_domains=' '.join(config.forte_domains),
                        domain=domain)
    put(conf, '/etc/nginx/sites-enabled/pianoforte.conf')
    restart(services='nginx')


@minicli.cli
def bootstrap():
    """Bootstrap a new server."""
    system()
    http()
    if config.ssl:
        letsencrypt()
        # Now put the https ready Nginx conf.
        http()
    ssh_keys()
    lxc_bootstrap()
    lxc_create(name='pianoforte')


@minicli.cli
def access_logs():
    """See the nginx access logs."""
    run('tail -F /var/log/nginx/access.log')


@minicli.cli
def error_logs():
    """See the nginx access logs."""
    run('tail -F /var/log/nginx/error.log')


@minicli.cli
def letsencrypt():
    """Configure letsencrypt."""
    with sudo():
        run('add-apt-repository --yes ppa:certbot/certbot')
        run('apt update')
        run('apt install -y certbot')
    mkdir('/var/www/letsencrypt/.well-known/acme-challenge')
    domains = ','.join(list(config.piano_domains) + list(config.forte_domains))
    certbot_conf = template('remote/host/certbot.ini', domains=domains)
    put(certbot_conf, '/var/www/certbot.ini')
    run('certbot certonly -c /var/www/certbot.ini --non-interactive '
        '--agree-tos')


if __name__ == '__main__':
    main('pfetalab')
