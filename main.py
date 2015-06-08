# **************************************************************************** #
#                                                                              #
#                                                                              #
#    g1dns.py                                                                  #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/02 18:44:39 by gmangin                                   #
#    Updated: 2015/06/08 17:55:42 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3.4 -w

import  sys
import re

PATH_READ='./Sample/'
PATH_WRITE='./ReadyToCopyPaste/'

FILE_OPTIONS='named.conf.options'
FILE_LOCAL='named.conf.local'
FILE_DB='db.' #+domain name !

CONF='./Conf/conf'


class ServerDns:
    def __init__(self):
        self._ip=''
        self.__domain_name=''
        self.__master=''
        self.__slaves=[]
        self.__subdomain=[]
        self.__is_master=True
        
    def set_ip(self, ip):
        self.__ip = ip

    def set_domain_name(self, name):
        self.__domain_name = name

    def set_master(self, master):
        self.__master = master

    def set_slaves(self, slave):
        self.__slaves.append(slave)

    def set_suddomain(self, subdomain):
        self.__subdomain.append(subdomain)

    def sef_ismaster(self, is_master):
        if is_master == True:
            set_master(self._ip)
        else:
            self.__is_master=False
            
    def write_local(self):
        '''it will fullfill FILE_LOCAL with domain_name, master and slaves informations'''
        pass
    
    def write_option(self):
        '''it will fullfill FILE_OPTIONS with master and slaves informations'''
        pass

    def write_db(self):
        '''it will fullfill FILE_DB with domain_name, master, slaves and subdomain informations'''
        pass
        
        
def launch_subdomaine_script(domain, sub_name, sud_ip):
    pass
#    dns = ServerDNS()

def ip_check(line, error):
    try:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
        print(ip[0])
        return ip[0]
    except IndexError:
        print('Please fullfill well the conf file, {}'.format(error))
        raise
        


def func_ip_serveur(dns, conf, line):
    dns.set_ip(ip_check(line, 'missing IP_SERVEUR !'))

def func_dns(dns, conf, line):
    try:
        isdns = re.findall(': (.+)', line)
        if isdns:
            dns.set_domain_name(isdns[0])
            print(isdns[0])
        else :
            error = 'MISSING DNS --> your domain s name {!r} '.format(line)
            raise NameError(error)
    except NameError as err:
        print(err)
        raise

def func_master(dns, conf, line):
    if re.search('YES', line):
        dns.set_ismaster(True)
    else :
        dns.set_ismaster(False)
        dns.set_master(ip_check(line, 'missing YES or IP MASTER !'))
        
def func_slave(dns, conf, line):
    if re.search('YES', line):
#        dns.set_slaves('YES') penser au cas ou c est un slave ...
        print('slaves YES')
    elif re.search('NO', line):
        print(' slave NO') # rien ne se passe ^^
    else :
         dns.set_slaves(ip_check(line, 'missing YES NO or IP SLAVE !'))
        
def func_sub_name(dns, conf, line): # il reste encore ce cas a faire ! les doneees a rentrer !
    try :
        print(line)
        sub_ip = conf.readline()
        if 'SUB_IP' in sub_ip:
            print(sub_ip)
        else:
            error = 'MISSING SUB_IP - the ip of the subdomain {!r}'.format(line)
            raise NameError(error)
    except NameError as err:
        print(err)
        raise
        
def launch_dns_script():
    with open(CONF, 'r') as conf:
        dns = ServerDns()
        funcdict={
            'IP_SERVEUR' : func_ip_serveur,
            'DNS' : func_dns,
            'MASTER' : func_master,
            'SLAVE' : func_slave,
            'SUB_NAME' : func_sub_name
        }
        for line in conf:
            for name in funcdict:
                if name in line : funcdict[name](dns, conf, line)

def print_usage():
    print("""\
Usage: {} [OPTIONS]
      -add [domain name] [subdomain name] [subdomain ip]
           Add a subdomain without changing anything
           on one domain of your dns server.
      
      READ THE README
    """.format(sys.argv[0]))

def main():
    try:
        if len(sys.argv) == 1:
            launch_dns_script()
        elif len(sys.argv) == 5 and sys.argv[1] == '-add':
            launch_subdomaine_script(sys.argv[2], sys.argv[3], sys.argv[4])
        else :
            print_usage()
    except:
        print('oups...')
            
if __name__ == '__main__':
    status = main()
    sys.exit(status)
    
