import argparse
from pathlib import Path
from pathlib import PurePath
import os

DIR_READ = Path('Conf')
DIR_WRITE = Path('ReadyToCopyPaste')

FILE_OPTIONS = 'conf'
FILE_LOCAL = "named.conf.local"
FILE_DB = "db.sample"
FILE_CONF = 'conf'

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

def parse_arg(parser, obj):
    parser.add_argument(obj,
                        nargs=2,
                        metavar=(':', 'VALUE'))

if __name__ == '__main__':
    path_conf = os.path.join(os.getcwd(), FILE_CONF)
    with open(path_conf, 'r') as conf:
        parser = argparse.ArgumentParser(description='Read the README.md before.')
        parse_arg(parser, 'IP_SERVER')
        parse_arg(parser, 'DNS')
        parse_arg(parser, 'MASTER')
        parse_arg(parser, 'SLAVE')
        parse_arg(parser, 'SUB_NAME')
        parse_arg(parser, 'SUB_IP')
    parser.add_argument('#',
                        nargs=+,
        args = parser.parse_args(conf)
        print(args)
        print(args.add)
