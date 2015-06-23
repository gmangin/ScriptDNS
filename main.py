#
#                                                                              #
#    Created: 2015/06/09 17:33:49 by gmangin                                   #
#    Updated: 2015/06/24 00:31:17 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3 -w

import re
import os
import sys
import argparse
import ipaddress

DIR_READ = 'Sample'
DIR_WRITE = 'ReadyToCopyPaste'

FILE_OPTIONS = "named.conf.options"
FILE_LOCAL = "named.conf.local"
FILE_DB = "db.sample"
FILE_CONF = 'conf'


class ServerDns(object):
    def __init__(self):
        self._ip = ''
        self._domain_name = ''
        self._master = ''
        self._slaves = []
        self._subdomain = {}
        self._is_master = True

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @property
    def domain_name(self):
        return self._domain_name

    @domain_name.setter
    def domain_name(self, name):
        self._domain_name = name

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, master):
        self._master = master

    @property
    def slaves(self):
        return self._slaves

    @slaves.setter
    def slaves(self, slave):
        self._slaves.append(slave)

    @property
    def subdomain(self):
        return self._subdomain

    @subdomain.setter
    def subdomain(self, sub_name):
        for key in sub_name:
            self._subdomain[key] = sub_name[key]

    @property
    def is_master(self):
        return self._is_master

    @is_master.setter
    def is_master(self, is_master):
        if is_master:
            self.master = self._ip
        else:
            self._is_master = False

    def __repr__(self):
        '''Print all the odject s attribut'''
        print('-Ip          : {}'.format(self._ip))
        print('-Domain_name : {}'.format(self._domain_name))
        print('-Master      : {}'.format(self._master))
        if self._slaves:
            print('-Slaves      : ')
            for slave in self._slaves:
                print('  * {}'.format(slave))
        if self._subdomain:
            print('-Subdomain   : ')
            for sub_name, sub_ip in self._subdomain.items():
                print('  * {0:8} = {1:}'.format(sub_name, sub_ip))
        if self._is_master:
            return 'I am the master !'
        else:
            return 'I am only a slave !'

    def replace_ip(self, line):
        '''Replace in Sample FILE the value _IP_SERVER_'''
        array = []
        array.append(line.replace('_IP_SERVER_', self.ip))
        return array

    def replace_domain_name(self, line):
        '''Replace in Sample FILE the value _DOMAIN_NAME_
           if there is many slave it will add ns+number automatically'''
        array = []
        if 'IN' and 'ns?.' in line:
            for index, value in enumerate(self.slaves):
                replace_domain = str(index + 2) + '.' + self.domain_name
                array.append(line.replace('?._DOMAIN_NAME_', replace_domain))
        else:
            array.append(line.replace('_DOMAIN_NAME_', self.domain_name))
        return array

    def replace_master(self, line):
        '''Replace in Sample FILE the value _MASTER_'''
        array = []
        array.append(line.replace('_MASTER_', self.master))
        return array

    def replace_slaves(self, line):
        '''Replace in Sample FILE the value _SLAVE_'''
        array = []
        for index, value in enumerate(self.slaves):
            if 'IN' and 'ns?' in line:
                test = line.replace('?', str(index + 2))
                array.append(test.replace('_SLAVE_', value))
            else:
                array.append(line.replace('_SLAVE_', value))
        return array

    def replace_subdomain(self, line):
        '''Replace in Sample FILE the value _SUB_NAME_ and _SUB_IP_'''
        array = []
        for name in self._subdomain:
            test = line.replace('_SUB_NAME_', name)
            array.append(test.replace('_SUB_IP_', self._subdomain[name]))
        return array

    def replace_value(self, line, destination):
        funcdict = {
            '_IP_SERVER_': self.replace_ip,
            '_DOMAIN_NAME_': self.replace_domain_name,
            '_MASTER_': self.replace_master,
            '_SLAVE_': self.replace_slaves,
            '_SUB_NAME_': self.replace_subdomain,
        }
        find = 0
        for name in funcdict:
            if name in line:
                array = funcdict[name](line)
                for item in array:
                    lines = destination.write(item)
                    find = 1
        if not find:
            destination.write(line)

    def get_file_local(self, destination):
        '''Open the correct FILE_LOCAL (master or slave)
           and call replace() to fullfill FILE_LOCAL info'''
        if self.is_master:
            file_local = 'master.{}'.format(FILE_LOCAL)
        else:
            file_local = 'slave.{}'.format(FILE_LOCAL)
        path_read_local = os.path.join(os.getcwd(), DIR_READ, file_local)
        with open(path_read_local, 'r') as source:
            for line in source:
                self.replace_value(line, destination)

    def get_file_options(self, destination, line):
        '''fullfill FILE_OPTIONS with master and slaves info'''
        self.replace_value(line, destination)

    def get_file_db(self, line, isdomain):
        '''fullfill FILE_DB with domain_name, master,
           slaves and subdomain info'''
        write_file_db = FILE_DB.replace('sample', self.domain_name)
        if isdomain:
            path_write_db = os.path.join(isdomain, write_file_db)
        else:
            path_write_db = os.path.join(os.getcwd(), DIR_WRITE, write_file_db)
        with open(path_write_db, 'a') as destination:
            self.replace_value(line, destination)

def file_local(all_dns, isdomain):
    '''Prepare the local file, send it to dns.get_file_local to be written
       Call from'''
    print('\n=== Getting the local file ===')
    if isdomain:
        path_write_local = os.path.join(isdomain, FILE_LOCAL)
    else:
        path_write_local = os.path.join(os.getcwd(), DIR_WRITE, FILE_LOCAL)
    with open(path_write_local, 'a') as destination:
        for dns in all_dns:
            dns.get_file_local(destination)
    print('Writting {} in {} directory'.format(FILE_LOCAL, isdomain))


def global_dns_ip(all_dns):
    '''Create a new dns instance with the ip server(dns.ip) and the
       others ip involve in all the dns (dns.slaves)
       CALL FROM file_option'''
    globalDns = ServerDns()
    for dns in all_dns:
        globalDns.ip = dns.ip
        #in order to avoid doublon, check if the ip is not already registered
        if not dns.is_master and dns.master not in globalDns.slaves:
            globalDns.slaves = dns.master
        else:
            for slave in dns.slaves:
                if slave != dns.ip and slave not in globalDns.slaves:
                    globalDns.slaves = slave
    return globalDns


def file_option(all_dns, isdomain):
    '''Create a new dns instance with the ip server(dns.ip) and the
       others ip involve in all the dns (dns.slaves) in order to
       fullfill FILE_OPTIONS
       CALL FROM'''
    print('\n=== Getting the options file ===')
    globalDns = global_dns_ip(all_dns)
    print(globalDns) # a faire un jolie print option quand meme ^^
    if isdomain:
        path_write_options = os.path.join(isdomain, FILE_OPTIONS)
    else:
        path_write_options = os.path.join(os.getcwd(), DIR_WRITE, FILE_OPTIONS)
    path_read_options = os.path.join(os.getcwd(), DIR_READ, FILE_OPTIONS)
    with open(path_write_options, 'a') as destination:
        with open(path_read_options, 'r') as source:
            for line in source:
                globalDns.get_file_options(destination, line)
            print('Writting {} in {} directory'.format(FILE_OPTIONS, isdomain))

def file_db(all_dns, isdomain):
    '''Open the sample file for db
       And send line by line to each instance get_file_db
       CALL FROM'''
    print('\n=== Getting the db file ===')
    path_read_db = os.path.join(os.getcwd(), DIR_READ, FILE_DB)
    with open(path_read_db, 'r') as source:
        for line in source:
            for dns in all_dns:
                if dns.is_master:
                    dns.get_file_db(line, isdomain)
        print('Writting the db file in {} directory'.format(isdomain))


def ip_check(line, error):
    '''Check if there is an ip in the line, if not return an exception
       CALL FROM func_ip_server, func_master, func_slave, func_sub_name'''
    try:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
        ipaddress.ip_address(ip[0])
        return ip[0]
    except:
        print('{} - {!r}'.format(error, line))
        raise


def parse_ip_server(dns, line):
    '''get the server ip from the conf file
       CALL FROM conf_parser'''
    dns.ip = ip_check(line, 'MISSING IP_SERVER')
    return None


def parse_dns(dns, line):
    '''get the domaine name from the conf file
       if it is a new dns, an new instance is created return
       CALL FROM conf_parser'''
    isdns = re.findall(': (.+)', line)
    if isdns:
        if dns.domain_name:
            newDns = ServerDns()
            newDns.ip = dns.ip
            newDns.domain_name = isdns[0]
            return newDns
        else:
            dns.domain_name = isdns[0]
    else:
        error = 'MISSING DNS - domain s name {!r} '.format(line)
        raise NameError(error)
    return None


def parse_master(dns, line):
    '''get the master ip from the conf file
       CALL FROM conf_parser'''
    if re.search('YES', line):
        dns.is_master = True
    else:
        dns.is_master = False
        dns.master = ip_check(line, 'MISSING YES or IP MASTER')
    return None


def parse_slave(dns, line):
    '''get the slave ip from the conf file if there is/are slave(s)
       CALL FROM conf_parser'''
    if not re.search('YES', line) and not re.search('NO', line):
        dns.slaves = ip_check(line, 'MISSING YES NO or IP SLAVE')
    return None


def parse_sub_name(dns, line):
    '''get the subdomain name and ip from the conf file
       if there is/are subdomain(s)
       CALL FROM conf_parser'''
    sub_name = re.findall(': (.+)', line)
    if not sub_name:
        error = 'MISSING SUB_NAME - subdomain\'s name {!r} '.format(line)
        raise NameError(error)
    dns.subdomain = {sub_name[0]: ''}
    return None


def parse_sub_ip(dns, line):
    for name in dns.subdomain:
        if dns.subdomain[name] == '':
            ip = ip_check(line, 'MISSING subdomain\'s ip')
            dns.subdomain[name] = ip
            return None
    error = 'MISSING SUB_IP - subdomain\'s ip {!r}'.format(line)
    raise NameError(error)


def check_conf(all_dns):
    for dns in all_dns:
        if not dns.ip or not dns.master or not dns.domain_name:
            error = 'Conf not valid !'
            raise NameError(error)
        

def parse_conf(all_dns, conf):
    '''Parse the conf file in order to get all the dns attribut
       CALL FROM file_conf'''
    funcdict = {
        'IP_SERVER': parse_ip_server,
        'DNS': parse_dns,
        'MASTER': parse_master,
        'SLAVE': parse_slave,
        'SUB_NAME': parse_sub_name,
        'SUB_IP': parse_sub_ip
    }
    dns = ServerDns()
    all_dns.append(dns)
    for line in conf:
        for name in funcdict:
            if name in line:
                newDns = funcdict[name](dns, line)
                if newDns:
                    all_dns.append(newDns)
                    dns = newDns


def print_dns(all_dns):
    for dns in all_dns:
        print('\n= NEW DNS =')
        print(dns)


def file_conf():
    '''read and Parse the conf file in order to get all the dns attribut
       all_dns[] contains all the DOMAIN NAME of the conf
       CALL FROM launch_dns_script()'''
    print('=== Getting the conf ===')
    all_dns = []
    path_conf = os.path.join(os.getcwd(), FILE_CONF)
    with open(path_conf, 'r') as conf:
        parse_conf(all_dns, conf)
    check_conf(all_dns)
    print_dns(all_dns)
    return(all_dns)


def launch_dns_script(isdomain):
    '''start to deploy dns server with the file conf
       and write all the dns file.
       all_dns[] contains all the DOMAIN NAME of the conf
       if the domain option is active, we check is the path is correct
       CALL FROM main'''
    all_dns = file_conf()
    file_local(all_dns, isdomain)
    file_db(all_dns, isdomain)
    file_option(all_dns, isdomain)


def init_args_parser(args):
    '''parse the sys.args with argparse and return the result
       CALL FROM main()'''
    parser = argparse.ArgumentParser(description='Read the README.md before.')
    help_parse ='''Add a domain on your dns server, Please launch on root
    the script And add the path of your bind9 conf Ex: -domain \'/etc/bind/\''''
    parser.add_argument('-domain',
                        nargs=1,
                        metavar='PATH_BIND_CONF',
                        help=help_parse)
    option = parser.parse_args(args)
    if option.domain and not os.path.isdir(option.domain[0]):
        raise NameError('this path is not correct : {!r}'.format(option.domain[0]))
    elif option.domain:
        return option.domain[0]
    else:
        return ''


def main():
    '''launch the domain script if option -domain,
       launch the dns script if no option
       and handle any error that happen during the program'''
    try:
        launch_dns_script(init_args_parser(sys.argv[1:]))
    except OSError as err:
            print("OS error: {0}".format(err))
    except NameError as err:
        print(err)
    except ValueError as err:
        print(err)
    except TypeError as err:
        print(err)
    except AttributeError as err:
        print(err)
    except:
        print('Goodbye, world! ', sys.exc_info()[0])

if __name__ == '__main__':
    status = main()
    sys.exit(status)
