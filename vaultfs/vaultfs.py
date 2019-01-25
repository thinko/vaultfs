import argparse
from fuse import FUSE
import vaultfs
from vaultfs.vault_fuse import vault_fuse
from vaultfs.vault_api import check_remote, check_local

def vaultfs(mountpoint, local, remote, payload, secrets_path):
    FUSE(vault_fuse(local, remote, payload, secrets_path), mountpoint, nothreads=True,
         foreground=True)

def main():

    # FIXME implement the possibility to get parameters via a config file
    
    parser = argparse.ArgumentParser(description='Vault fuse file system')

    parser.add_argument( '-c', '--config', dest='config', metavar='', required=False, help='Config file.')
    parser.add_argument( '-m', '--mountpoint', dest='mountpoint', metavar='',
        required=True, help='where the fuse filesystem will be mounted.')
    parser.add_argument( '-l', '--local', dest='local', metavar='', required=True,
                        help='credentials local path after being pulled from vault.')
    parser.add_argument( '-r', '--remote', dest='remote', metavar='', required=True, help='Vault Server HTTPS address.')
    parser.add_argument( '-s', '--secrets-path', dest='secrets_path', metavar='', required=True,
        action='append', help='List of secrets path in the Vault server.')
    parser.add_argument( '-p', '--payload', dest='payload', metavar='', required=True,
        help='.Vault authentication token')

    args = parser.parse_args()

    config_file = ConfigParser()
    if args.config:
        config_file.read(args.config)

    # print (config_file.sections())
    # print(config_file.get("main", 'param'))
    # print(config_file.["main"]['param']

    # FIXME: Add some controls over mountpoint/local (should be a folder), remote should be reachable payload should exist
    mountpoint = args.mountpoint
    local = args.local
    remote = args.remote.rstrip('/')
    secrets_path = args.secrets_path
    payload = args.payload

    # initial checks
    check_remote(remote)
    check_local(local)
    check_local(mountpoint)

    vaultfs(mountpoint, local, remote,  payload, secrets_path)


if __name__ == '__main__':

    main()
