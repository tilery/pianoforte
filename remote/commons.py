import minicli
import requests
from usine import config, connect, put, run, sudo


def service(name):
    with sudo():
        put(f'remote/{name}.service', f'/etc/systemd/system/{name}.service')
        systemctl(f'enable {name}.service')


@minicli.cli
def ssh_keys():
    """Install ssh keys from remote urls."""
    with sudo():
        for name, url in config.get('ssh_key_urls', {}).items():
            key = requests.get(url).text.replace('\n', '')
            run('grep -q -r "{key}" .ssh/authorized_keys || echo "{key}" '
                '| tee --append .ssh/authorized_keys'.format(key=key))


@minicli.cli
def systemctl(*args):
    """Run a systemctl command on the remote server.

    :command: the systemctl command to run.
    """
    run(f'systemctl {" ".join(args)}')


@minicli.cli
def restart(services=None):
    """Restart services."""
    services = services or 'renderd apache2 imposm munin-node'
    with sudo():
        systemctl(f'restart {services}')


@minicli.wrap
def wrapper(hostname, configpath):
    with connect(hostname=hostname, configpath=configpath):
        yield


def main(hostname):
    minicli.run(hostname='tilery', configpath='remote/config.yml')
