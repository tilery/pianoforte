import minicli
from usine import config, exists, put, run, sudo, template, mkdir

from ..commons import main, ssh_keys, restart


@minicli.cli
def system():
    """Install the host system deps."""
    # Not installed in minimized 18.04.
    run('which sudo || apt install sudo')
    with sudo():
        run('apt update')
        run('apt install -y nginx lxc')
        mkdir('/data')  # Should be already done by the partionning.


def lxc_bootstrap():
    put('remote/host/lxc-net', '/etc/default/lxc-net')
    put('remote/host/dnsmasq-hosts.conf', '/etc/lxc/dnsmasq-hosts.conf')
    put('remote/host/dnsmasq.conf', '/etc/lxc/dnsmasq.conf')
    restart('lxc-net')


@minicli.cli
def lxc_create(name, ip):
    """Install and configure an LXC container."""
    if name not in run('lxc-ls'):
        mkdir(f'/data/lxc/{name}')
        run(f'lxc-create --name {name} --dir /data/lxc/{name} '
            f'--template download -- -d ubuntu -r bionic -a amd64')
        path = f'/var/lib/lxc/{name}/config'
        line = f'lxc.apparmor.allow_incomplete = 1'
        run(f'grep -q -r "{line}" {path} '
            f'|| echo "{line}" | tee --append {path}')
        run(f'lxc-start -n {name}')
    run(f'lxc-attach -n {name} -- apt install -y openssh-server')
    mkdir(f'/data/lxc/{name}/root/.ssh/')
    run(f'cp /root/.ssh/authorized_keys '
        f'/data/lxc/{name}/root/.ssh/')


@minicli.cli
def http():
    """Configure Nginx and letsencrypt."""
    # When we'll have a domain.
    put('remote/nginx.conf', '/etc/nginx/snippets/pianoforte.conf')
    put('remote/letsencrypt.conf', '/etc/nginx/snippets/letsencrypt.conf')
    put('remote/ssl.conf', '/etc/nginx/snippets/ssl.conf')
    domains = ' '.join(config.domains)
    domain = config.domains[0]
    pempath = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
    if exists(pempath):
        print(f'{pempath} found, using https configuration')
        conf = template('remote/nginx-https.conf', domains=domains,
                        domain=domain)
    else:
        print(f'{pempath} not found, using http configuration')
        # Before letsencrypt.
        conf = template('remote/nginx-http.conf', domains=domains,
                        domain=domain)
    put(conf, '/etc/nginx/sites-enabled/default')
    restart(services='nginx')


@minicli.cli
def bootstrap():
    """Bootstrap a new server."""
    system()
    http()
    # if config.ssl:
    #     letsencrypt()
    #     # Now put the https ready Nginx conf.
    #     http()
    ssh_keys()
    lxc_bootstrap()
    lxc_create(name='pianoforte', ip='10.10.10.10')


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
    certbot_conf = template('remote/certbot.ini',
                            domains=','.join(config.domains))
    put(certbot_conf, '/srv/tilery/certbot.ini')
    put('remote/ssl-renew', '/etc/cron.weekly/ssl-renew')
    run('chmod +x /etc/cron.weekly/ssl-renew')
    run('certbot certonly -c /srv/tilery/certbot.ini --non-interactive '
        '--agree-tos')


if __name__ == '__main__':
    main('pfetalab')
