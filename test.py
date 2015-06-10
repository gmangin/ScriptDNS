import argparse
from pathlib import Path
from pathlib import PurePath
import os

DIR_READ = Path('Conf')
DIR_WRITE = Path('ReadyToCopyPaste')

FILE_OPTIONS = 'conf'
FILE_LOCAL = "named.conf.local"
FILE_DB = "db.sample"


class ServerDns(object):
    def __init__(self):
        self._ip = ''

    @property
    def ip(self):
        '''I'm the 'ip' property'''
        print("Getting value")
        return self._ip

    @ip.setter
    def ip(self, ip):
        print("setting value")
        self._ip = ip

    def __repr__(object):
        print('prout')
        return ''

if __name__ == '__main__':
#    dns = ServerDns()
#    dns.ip = 'caca'
#    print(dns.ip)
#    print(dns)

    parser = argparse.ArgumentParser(description='Read the README.md before.')
    metavar_parse = ('DOMAIN_NAME', 'SUBDOMAIN_NAME', 'SUBDOMAIN_IP')
    help_parse = 'Add a subdomain on one domain of your dns server.'
    parser.add_argument('-add',
                        nargs=3,
                        metavar=metavar_parse,
                        dest='add',
                        help=help_parse)
    args = parser.parse_args()
    print(args)
    print(args.add)
