PATH_READ="./Sample/"
PATH_WRITE="./ReadyToCopyPaste/"

FILE_OPTIONS="named.conf.options"
FILE_LOCAL="named.conf.local"
FILE_DB="db." #+domain name !

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

#    def __repr__(object):
#        print('prout')
#        return ''

if __name__ == '__main__':
    dns = ServerDns()
    dns.ip = 'caca'
    print(dns.ip)
    print(dns)
