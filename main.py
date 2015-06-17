# **************************************************************************** #
#                                                                              #
#                                                                              #
#    main.py                                                                   #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/09 17:33:49 by gmangin                                   #
#    Updated: 2015/06/17 16:57:26 by gmangin                                   #
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
    def suddomain(self):
        return self._subdomain

    @suddomain.setter
    def suddomain(self, sub_name):
        for key in sub_name:
            self._subdomain[key] = sub_name[key]

    @property
    def ismaster(self):
        return self._is_master

    @ismaster.setter
    def ismaster(self, is_master):
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
        return '-Is_master   : {}'.format(self._is_master)

    def replace_ip(self, line, destination):
        destination.write(line.replace('__IP_SERVER__', self.ip))

    def replace_domain_name(self, line, destination):
        if 'IN' and 'ns?.' in line:
            for index, value in enumerate(self.slaves):
                replace_domain = str(index + 2) + '.' + self.domain_name
                destination.write(line.replace('?.__DOMAIN_NAME__',
                                               replace_domain))
        else:
            destination.write(line.replace('__DOMAIN_NAME__', self.domain_name))

    def replace_master(self, line, destination):
        destination.write(line.replace('__MASTER__', self.master))

    def replace_slaves(self, line, destination):
        for index, value in enumerate(self.slaves):
            if 'IN' and 'ns?' in line:
                test = line.replace('?', str(index + 2))
                destination.write(test.replace('__SLAVE__', value))
            else:
                destination.write(line.replace('__SLAVE__', value))

    def replace_suddomain(self, line, destination):
        for name in self._subdomain:
            keep = line
            test = keep.replace('__SUB_NAME__', name)
            destination.write(test.replace('__SUB_IP__', self._subdomain[name]))

    def replace_ismaster(self, line, destination):
        if self.ismaster:
            destination.write(line.replace('__ISMASTER__', self.master))

    def replace_value(self, line, destination):
        funcdict = {
            '__IP_SERVER__': self.replace_ip,
            '__DOMAIN_NAME__' : self.replace_domain_name,
            '__MASTER__' : self.replace_master,
            '__SLAVE__' : self.replace_slaves,
            '__SUB_NAME__' : self.replace_suddomain,
            '__ISMASTER__' : self.replace_ismaster
        }
        find = 0
        for name in funcdict:
            if name in line:
                print(name)
                funcdict[name](line, destination)
                find = 1
        if not find:
            destination.write(line)
                    
    def get_file_local(self, destination):
        '''Open the correct FILE_LOCAL (master or slave)
           and call replace() to fullfill FILE_LOCAL info'''
        if self.ismaster:
            file_local = 'master.{}'.format(FILE_LOCAL)
        else:
            file_local = 'slave.{}'.format(FILE_LOCAL)
        path_read_local = os.path.join(os.getcwd(), DIR_READ, file_local)
        with open(path_read_local, 'r') as source:
            for line in source:
                self.replace_value(line, destination)

    def get_file_option(self):
        '''fullfill FILE_OPTIONS with master and slaves info'''
        path_read_options = os.path.join(os.getcwd(), DIR_READ, FILE_OPTIONS)

    def get_file_db(self, line):
        '''fullfill FILE_DB with domain_name, master,
           slaves and subdomain info'''
        if self.ismaster:
            write_file_db = FILE_DB.replace('sample', self.domain_name)
            path_write_db = os.path.join(os.getcwd(), DIR_WRITE, write_file_db)
            with open(path_write_db, 'a') as destination:
                self.replace_value(line, destination)


def file_local(all_dns, isdomain):
    '''Prepare the local file, send it to dns.get_file_local to be written
       Call from'''
    print('=== Getting the local file ===')
    path_write_local = os.path.join(os.getcwd(), DIR_WRITE, FILE_LOCAL)
    with open(path_write_local, 'a') as destination:
        for dns in all_dns:
            dns.get_file_local(destination)


def file_option(all_dns, isdomain):
    print('=== Getting the options file ===')
    path_write_options = all_dns, os.path.join(os.getcwd(), DIR_WRITE, FILE_OPTIONS)
    with open(path_write_options, 'a') as destination:
        for dns in all_dns:
            dns.get_file_options(destination)


def file_db(all_dns, isdomain):
    '''Open the sample file for db
       And send line by line to each instance get_file_db
       CALL FROM'''
    print('=== Getting the db file ===')
    path_read_db = os.path.join(os.getcwd(), DIR_READ, FILE_DB)
    with open(path_read_db, 'r') as source:
        for line in source:
            for dns in all_dns:
                dns.get_file_db(line)


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


def parse_ip_server(dns, conf, line):
    '''get the server ip from the conf file
       CALL FROM conf_parser'''
    dns.ip = ip_check(line, 'MISSING IP_SERVER')


def parse_dns(dns, conf, line):
    '''get the domaine name from the conf file
       CALL FROM conf_parser'''
    isdns = re.findall(': (.+)', line)
    if isdns:
        dns.domain_name = isdns[0]
    else:
        error = 'MISSING DNS - domain s name {!r} '.format(line)
        raise NameError(error)


def parse_master(dns, conf, line):
    '''get the master ip from the conf file
       CALL FROM conf_parser'''
    if re.search('YES', line):
        dns.ismaster = True
    else:
        dns.ismaster = False
        dns.master = ip_check(line, 'MISSING YES or IP MASTER')


def parse_slave(dns, conf, line):
    '''get the slave ip from the conf file if there is/are slave(s)
       CALL FROM conf_parser'''
    if not re.search('YES', line) and not re.search('NO', line):
        dns.slaves = ip_check(line, 'MISSING YES NO or IP SLAVE')


def parse_sub_name(dns, conf, line):
    '''get the subdomain name and ip from the conf file
       if there is/are subdomain(s)
       CALL FROM conf_parser'''
    sub_name = re.findall(': (.+)', line)
    if not sub_name:
        error = 'MISSING SUB_NAME - subdomain\'s name {!r} '.format(line)
        raise NameError(error)
    sub_ip = conf.readline()
    if 'SUB_IP' in sub_ip:
        ip = ip_check(sub_ip, 'MISSING subdomain\'s ip')
        dns.suddomain = {sub_name[0]: ip}
    else:
        error = 'MISSING SUB_IP - subdomain\'s ip {!r}'.format(line)
        raise NameError(error)


def file_conf(all_dns):
    '''read and Parse the conf file in order to get all the dns attribut
       CALL FROM launch_dns_script()'''
    dns = ServerDns()
    all_dns.append(dns)
    print('=== Getting the conf ===')
    path_conf = os.path.join(os.getcwd(), FILE_CONF)
    with open(path_conf, 'r') as conf:
        funcdict = {
            'IP_SERVER': parse_ip_server,
            'DNS': parse_dns,
            'MASTER': parse_master,
            'SLAVE': parse_slave,
            'SUB_NAME': parse_sub_name
        }
        for line in conf:
            for name in funcdict:
                if name in line:
                    funcdict[name](dns, conf, line)
    for dns in all_dns:
        print(dns)


def launch_dns_script(isdomain):
    '''start to deploy dns server with the file conf
       and write all the dns file.
       all_dns[] contains all the DOMAIN NAME of the conf
       CALL FROM main'''
    all_dns = []
    file_conf(all_dns)
    file_local(all_dns, isdomain)
#    file_option(all_dns, isdomain) not done yet
    file_db(all_dns, isdomain)


def init_args_parser(args):
    '''parse the sys.args with argparse and return the result
    CALL FROM main()'''
    parser = argparse.ArgumentParser(description='Read the README.md before.')
    metavar_parse = ('DOMAIN_NAME', 'SUBDOMAIN_NAME', 'SUBDOMAIN_IP')
    help_parse = 'Add a domain on your dns server, please launch on root the script and add the path of your bind9 conf ex: -domain \'/etc/bind/\''
    parser.add_argument('-domain',
                        nargs=1,
                        metavar='PATH_BIND_CONF',
                        help=help_parse)
    return parser.parse_args(args)


def main():
    '''launch the domain script if option -domain,
       launch the dns script if no option
       and handle any error that happen during the program'''
    try:
        args = init_args_parser(sys.argv[1:])
        print(args)
        launch_dns_script(args.domain)
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
