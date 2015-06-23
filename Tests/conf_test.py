# **************************************************************************** #
#                                                                              #
#                                                                              #
#    conf_test.py                                                              #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/18 14:12:03 by gmangin                                   #
#    Updated: 2015/06/23 23:20:08 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

#ici sera tester la conf

# conf dans le desordre

#conf avec plusieurs DOMAIN NAME, 2 bien remplis, et aussi 2 mal remplis pour voir ^^

import unittest
import sys
import os
import main
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

DIR_CONF = 'Conf'
FILE_CONF = 'conf'
DIR_TEST = 'Tests'

class TestFunctionFileConf(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_conf_empty(self):
        '''Test the program with an empty conf'''
        try:
            start_function('conf_empty')
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_dns_correct1(self):
        '''Test parse_dns() function with one dns'''
        dns = main.ServerDns()
        line = 'DNS  : unicorn'
        main.parse_dns(dns, line)
        self.assertEqual(dns.domain_name, 'unicorn')

    def test_parse_dns_correct2(self):
        '''Test parse_dns() function with many dns'''
        dns = main.ServerDns()
        line = 'DNS  : unicorn'
        main.parse_dns(dns, line)
        line = 'DNS  : coucou'
        check = main.parse_dns(dns, line)
        self.assertEqual(dns.domain_name, 'unicorn')
        self.assertEqual(check.domain_name, 'coucou')

    def test_parse_dns_no_correct(self):
        '''Test parse_dns() function with no DNS'''
        dns = main.ServerDns()
        line = 'DNS  : '
        try:
            main.parse_dns(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_sub_name_correct(self):
        '''Test parse_sub_name() function'''
        dns = main.ServerDns()
        line = 'SUB_NAME  : unicorn'
        main.parse_sub_name(dns, line)
        self.assertEqual(dns.subdomain, {'unicorn': ''})

    def test_parse_sub_name_no_correct(self):
        '''Test parse_sub_name() function with no SUB_NAME'''
        dns = main.ServerDns()
        line = 'SUB_NAME  : '
        try:
            main.parse_sub_name(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_sub_ip_correct(self):
        '''Test parse_sub_ip() function with correct conf'''
        dns = main.ServerDns()
        line = 'SUB_NAME  : unicorn'
        main.parse_sub_name(dns, line)
        line = 'SUB_IP  : 8.8.8.8'
        main.parse_sub_ip(dns, line)
        self.assertEqual(dns.subdomain, {'unicorn': '8.8.8.8'})

    def test_parse_sub_ip_no_correct0(self):
        '''Test parse_sub_name() function with no SUB_IP'''
        dns = main.ServerDns()
        line = 'SUB_IP  : '
        try:
            main.parse_sub_ip(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_sub_ip_no_correct1(self):
        '''Test parse_sub_name() function with no correct conf (no SUB_NAME)'''
        dns = main.ServerDns()
        line = 'SUB_IP  : 8.8.8.8'
        try:
            main.parse_sub_ip(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_sub_ip_no_correct2(self):
        '''Test parse_sub_name function with no correct conf wrong ip'''
        dns = main.ServerDns()
        line = 'SUB_NAME  : unicorn'
        main.parse_sub_name(dns, line)
        line = 'SUB_IP  : I am not an ip'
        try:
            main.parse_sub_ip(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_slave_correct(self):
        '''Test parse_slave() function with correct conf'''
        dns = main.ServerDns()
        line = 'SLAVE   : 8.8.8.8'
        main.parse_slave(dns, line)
        self.assertEqual(dns.slaves, ['8.8.8.8'])

    def test_parse_slave_no_correct1(self):
        '''Test parse_slave() function with no SLAVE'''
        dns = main.ServerDns()
        line = 'SLAVE  : '
        try:
            main.parse_slave(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_slave_no_correct2(self):
        '''Test parse_slave() function with wrong ip'''
        dns = main.ServerDns()
        line = 'SLAVE  : 8888.8.8.8'
        try:
            main.parse_slave(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_ip_server_no_correct1(self):
        '''Test parse_ip_server() function with no IP_SERVER'''
        dns = main.ServerDns()
        line = 'IP_SERVER  : '
        try:
            main.parse_ip_server(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_ip_server_no_correct2(self):
        '''Test parse_ip_server() function with wrong ip'''
        dns = main.ServerDns()
        line = 'IP_SERVER  : 999.8.8.8'
        try:
            main.parse_ip_server(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_master_correct(self):
        '''Test parse_master function with correct conf'''
        dns = main.ServerDns()
        line = 'MASTER   : 8.8.8.8'
        main.parse_master(dns, line)
        self.assertEqual(dns.master, '8.8.8.8')

    def test_parse_is_master_correct1(self):
        '''Test parse_master function with correct conf and server is slave'''
        dns = main.ServerDns()
        line = 'IP_SERVER   : 8.8.8.1'
        main.parse_ip_server(dns, line)
        line = 'MASTER   : 8.8.8.8'
        main.parse_master(dns, line)
        self.assertEqual(dns.is_master, False)

    def test_parse_is_master_correct2(self):
        '''Test parse_master function with correct conf and server is master'''
        dns = main.ServerDns()
        line = 'IP_SERVER   : 8.8.8.8'
        main.parse_ip_server(dns, line)
        line = 'MASTER   : YES'
        main.parse_master(dns, line)
        self.assertEqual(dns.is_master, True)

    def test_parse_master_no_correct1(self):
        '''Test parse_master() function with no MASTER'''
        dns = main.ServerDns()
        line = 'MASTER  : '
        try:
            main.parse_master(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_parse_master_no_correct2(self):
        '''Test parse_master() function with wrong ip'''
        dns = main.ServerDns()
        line = 'MASTER  : 999.8.8.8'
        try:
            main.parse_master(dns, line)
        except:
            pass
        else:
            self.fail('Did not see exception')

    def test_print_dns_master(self):
        '''Test if the conf parsing when well in the master case'''
        all_dns = start_function('conf_correct_sample_master')
        main.print_dns(all_dns)
        out = '''
= NEW DNS =
-Ip          : 8.8.8.8
-Domain_name : example.com
-Master      : 8.8.8.8
-Slaves      : 
  * 8.8.8.1
  * 8.8.8.2
-Subdomain   : 
  * test     = 8.8.8.10
I am the master !
'''
        self.assertEqual(sys.stdout.getvalue(), out)

    def test_print_dns_slave(self):
        '''Test if the conf parsing when well in the slave case'''
        all_dns = start_function('conf_correct_sample_slave')
        main.print_dns(all_dns)
        out = '''
= NEW DNS =
-Ip          : 8.8.8.8
-Domain_name : example.com
-Master      : 8.8.8.1
-Slaves      : 
  * 8.8.8.2
-Subdomain   : 
  * test     = 8.8.8.10
I am only a slave !
'''
        self.assertEqual(sys.stdout.getvalue(), out)

    def test_print_multiple_dns(self):
        '''Test if the conf parsing when well if mutiple dns'''
        all_dns = start_function('conf_correct_multiple')
        main.print_dns(all_dns)
        out = '''
= NEW DNS =
-Ip          : 8.8.8.8
-Domain_name : example.com
-Master      : 8.8.8.1
-Slaves      : 
  * 8.8.8.2
-Subdomain   : 
  * test     = 8.8.8.10
I am only a slave !

= NEW DNS =
-Ip          : 8.8.8.8
-Domain_name : coucou.com
-Master      : 8.8.8.8
I am the master !
'''
        self.assertEqual(sys.stdout.getvalue(), out)

    #not done yet !
    def test_file_conf(self):
        to_check = main.file_conf()
        self.assertNotEqual(to_check, [])


def start_function(here):
    all_dns = []
    path_conf = os.path.join(os.getcwd(), DIR_TEST, DIR_CONF, here, FILE_CONF)
    with open(path_conf, 'r') as conf:
        main.parse_conf(all_dns, conf)
        main.check_conf(all_dns)
    return all_dns



if __name__ == '__main__':
    unittest.main()
