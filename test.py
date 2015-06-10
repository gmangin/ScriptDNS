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
    dns = ServerDns()
    dns.ip = 'caca'
    print(dns.ip)
    print(dns)

#    print([x for x in p.iterdir() if x.is_dir()])
    p = PurePath(Path.cwd(), DIR_READ, FILE_OPTIONS)
    print(p)
#    print(list(p.glob('**/' FILE_OPTIONS)))
#    q = p / 'Sample' / FILE_OPTIONS
#    print(q)
#    print(q.resolve())
