# **************************************************************************** #
#                                                                              #
#                                                                              #
#    g1dns.py                                                                  #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/02 18:44:39 by gmangin                                   #
#    Updated: 2015/06/09 15:36:32 by gmangin                                   #
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
        self.__ip=''
        self.__domain_name=''
        self.__master=''
        self.__slaves=[]
        self.__subdomain={}
        self.__is_master=True
        
    def set_ip(self, ip):
        self.__ip = ip

    def set_domain_name(self, name):
        self.__domain_name = name

    def set_master(self, master):
        self.__master = master

    def set_slaves(self, slave):
        self.__slaves.append(slave)

    def set_suddomain(self, sub_name, sub_ip):
        self.__subdomain[sub_name] = sub_ip

    def set_ismaster(self, is_master):
        if is_master == True:
            self.set_master(self.__ip)
        else:
            self.__is_master=False

    def show_attribut(self):
        '''Print all the odject s attribut'''
        print('-Ip          : {}'.format(self.__ip))
        print('-Domain_name : {}'.format(self.__domain_name))
        print('-Master      : {}'.format(self.__master))
        print('-Is_master   : {}'.format(self.__is_master))
        if self.__slaves:
            print('-Slaves      : ')
            for slave in self.__slaves:
                print('  * {}'.format(slave))
        print('-Subdomain   : ')
        for sub_name, sub_ip in self.__subdomain.items():
            print('  * {0:8} = {1:}'.format(sub_name, sub_ip))

    def write_local(self):
        '''fullfill FILE_LOCAL with domain_name, master and slaves info'''
        pass
    
    def write_option(self):
        '''fullfill FILE_OPTIONS with master and slaves info'''
        pass

    def write_db(self):
        '''fullfill FILE_DB with domain_name, master,'''
        '''slaves and subdomain info'''
        pass

def launch_subdomaine_script(domain, sub_name, sud_ip):
    ''' '''
    '''CALL FROM main()'''
    pass
#    dns = ServerDNS()

def ip_check(line, error):
    '''check if there is an ip in the line, if not return an exception '''
    '''CALL FROM func_ip_serveur, func_master, func_slave, func_sub_name'''
    try:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
        return ip[0]
    except IndexError:
        print('{} - {}'.format(error, line))
        raise
        
def func_ip_serveur(dns, conf, line):
    '''get the server ip from the conf file '''
    '''CALL FROM conf_parser'''
    dns.set_ip(ip_check(line, 'MISSING IP_SERVEUR - {!r}'.format(line)))

def func_dns(dns, conf, line):
    '''get the domaine name from the conf file '''
    '''CALL FROM conf_parser'''
    try:
        isdns = re.findall(': (.+)', line)
        if isdns:
            dns.set_domain_name(isdns[0])
        else :
            error = 'MISSING DNS - domain s name {!r} '.format(line)
            raise NameError(error)
    except NameError as err:
        print(err)
        raise

def func_master(dns, conf, line):
    '''get the master ip from the conf file '''
    '''CALL FROM conf_parser'''
    if re.search('YES', line):
        dns.set_ismaster(True)
    else :
        dns.set_ismaster(False)
        dns.set_master(ip_check(line, 'MISSING YES or IP MASTER'))
        
def func_slave(dns, conf, line):
    '''get the slave ip from the conf file if there is/are slave(s)'''
    '''CALL FROM conf_parser'''
    if not re.search('YES', line) and not re.search('NO', line) :
         dns.set_slaves(ip_check(line, 'MISSING YES NO or IP SLAVE'))
        
def func_sub_name(dns, conf, line):
    '''get the subdomain name and ip from the conf file'''
    ''' if there is/are subdomain(s)'''
    '''CALL FROM conf_parser'''
    try :
        sub_name = re.findall(': (.+)', line)
        if not sub_name:
            error = 'MISSING SUB_NAME - subdomain\'s name {!r} '.format(line)
            raise NameError(error)
        sub_ip = conf.readline()
        if 'SUB_IP' in sub_ip:
            ip = ip_check(sub_ip, 'MISSING subdomain\'s ip')
            dns.set_suddomain(sub_name[0], ip)
        else:
            error = 'MISSING SUB_IP - subdomain\'s ip {!r}'.format(line)
            raise NameError(error)
    except NameError as err:
        print(err)
        raise

def conf_parser(dns):
    '''Parse the conf file in order to get all the dns attribut'''
    '''CALL FROM launch_dns_script()'''
    with open(CONF, 'r') as conf:
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
        dns.show_attribut()
    
def launch_dns_script():
    '''start to deploy dns server with the file conf'''
    '''and write all the dns file'''
    '''CALL FROM main'''
    dns = ServerDns()
    conf_parser(dns)
#    dns.write_local()
#    dns.write_option()
#    dns.write_db()

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
    
