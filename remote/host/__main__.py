import minicli
from usine import config, exists, put, run, sudo, template

from ..commons import main, ssh_keys, restart


@minicli.cli
def system():
    """Install the host system deps."""
    # Not installed in minimized 18.04.
    run('sudo --version || apt install sudo')
    with sudo():
        run('apt update')
        run('apt install -y nginx')


@minicli.cli
def http():
    """Configure Nginx and letsencrypt."""
    # When we'll have a domain.
    put('remote/nginx.conf', '/srv/tilery/nginx.conf')
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
    if config.ssl:
        letsencrypt()
        # Now put the https ready Nginx conf.
        http()
    ssh_keys()


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
    main('pianoforteqa')
