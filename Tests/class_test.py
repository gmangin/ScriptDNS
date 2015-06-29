# **************************************************************************** #
#                                                                              #
#                                                                              #
#    class_test.py                                                             #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/19 17:13:32 by gmangin                                   #
#    Updated: 2015/06/28 16:56:22 by gmangin                                   #
#                                                                              #
# **************************************************************************** #


import unittest
import main

class TestClass(unittest.TestCase):

    def test_replace_value1(self):
        '''Check replace_value function with no data'''
        dns = main.ServerDns()
        line = ''
        to_check = dns.replace_value(line)
        check = ['']
        self.assertEqual(to_check, check)

    def test_replace_value2(self):
        '''Check replace_value function with a simple line'''
        dns = main.ServerDns()
        line = 'coucou'
        to_check = dns.replace_value(line)
        check = ['coucou']
        self.assertEqual(to_check, check)

    def test_replace_value3(self):
        '''Check replace_value function with a line to replace'''
        dns = main.ServerDns()
        dns.ip = '8.8.8.8'
        line = '_IP_SERVER_'
        to_check = dns.replace_value(line)
        check = ['8.8.8.8']
        self.assertEqual(to_check, check)

    def test_replace_ip(self):
        '''Check replace_ip function with an ip'''
        dns = main.ServerDns()
        line = ' coucou _IP_SERVER_ coucou '
        to_check = dns.replace_ip(line)
        check = [' coucou  coucou ']
        self.assertEqual(to_check, check)

    def test_replace_domain_name_1(self):
        '''Check replace_domain_name when there s no NS? and no slave'''
        dns = main.ServerDns()
        dns.domain_name = 'example.com'
        line = ' coucou _DOMAIN_NAME_ coucou '
        to_check = dns.replace_domain_name(line)
        check = [' coucou example.com coucou ']
        self.assertEqual(to_check, check)

    def test_replace_domain_name_2(self):
        '''Check replace_domain_name function
           when there s NS? and no slave'''
        dns = main.ServerDns()
        dns.domain_name = 'example.com'
        line = '@       IN      NS      ns?._DOMAIN_NAME_.'
        to_check = dns.replace_domain_name(line)
        check = []
        self.assertEqual(to_check, check)

    def test_replace_domain_name_3(self):
        '''Check replace_domain_name function
           when there is NS? and many slaves'''
        dns = main.ServerDns()
        dns.domain_name = 'example.com'
        dns.slaves = '1.1.1.1'
        dns.slaves = '2.2.2.2'
        line = '@       IN      NS      ns?._DOMAIN_NAME_.'
        to_check = dns.replace_domain_name(line)
        check = ['@       IN      NS      ns2.example.com.',
                 '@       IN      NS      ns3.example.com.',]
        self.assertEqual(to_check, check)

    def test_replace_master(self):
        '''Check replace_master function'''
        dns = main.ServerDns()
        dns.master = '8.8.8.8'
        line = ' coucou _MASTER_ coucou '
        to_check = dns.replace_master(line)
        check = [' coucou 8.8.8.8 coucou ']
        self.assertEqual(to_check, check)

    def test_replace_slaves_1(self):
        '''Check replace_slaves function when there is no slaves
           in the conf file'''
        dns = main.ServerDns()
        line = ' coucou _SLAVES_ coucou '
        to_check = dns.replace_slaves(line)
        check = []
        self.assertEqual(to_check, check)

    def test_replace_slaves_2(self):
        '''Check replace_slaves function when there is many slaves
           in the conf file'''
        dns = main.ServerDns()
        dns.slaves = '1.1.1.1'
        dns.slaves = '2.2.2.2'
        line = ' coucou _SLAVE_ coucou '
        to_check = dns.replace_slaves(line)
        check = [' coucou 1.1.1.1 coucou ',
                 ' coucou 2.2.2.2 coucou ']
        self.assertEqual(to_check, check)

    def test_replace_slaves_3(self):
        '''Check replace_slaves function when there is many slaves
           in the conf file and ns? in the line'''
        dns = main.ServerDns()
        dns.slaves = '1.1.1.1'
        dns.slaves = '2.2.2.2'
        line = 'ns?     IN      A       _SLAVE_'
        to_check = dns.replace_slaves(line)
        check = ['ns2     IN      A       1.1.1.1',
                 'ns3     IN      A       2.2.2.2']
        self.assertEqual(to_check, check)

    def test_replace_subdomain_1(self):
        '''Check replace_subdomain function when there is no subdomain
           in the conf file'''
        dns = main.ServerDns()
        line = ' coucou _SUB_NAME_ coucou  _SUB_IP_ coucou '
        to_check = dns.replace_subdomain(line)
        check = []
        self.assertEqual(to_check, check)

    def test_replace_subdomain_2(self):
        '''Check replace_subdomain function when there is many subdomain
           in the conf file'''
        dns = main.ServerDns()
        dns.subdomain = {'unicorn': '8.8.8.8', 'Poney': '8.8.8.1'}
        line = ' coucou _SUB_NAME_ coucou  _SUB_IP_ coucou '
        to_check = dns.replace_subdomain(line)
        check = [' coucou unicorn coucou  8.8.8.8 coucou ',
                 ' coucou Poney coucou  8.8.8.1 coucou ']
        map(lambda x, y: self.assertAlmostEqual(x, y), to_check, check)


if __name__ == '__main__':
    unittest.main()

#   ==  GOOD TO KEEP ==
#        myfile = './ERASEME'
#        dns = main.ServerDns()
#        line = 'coucou _IP_SERVER_ coucou '
#        with open(myfile, 'a+') as destination:
#            dns.replace_ip(line, destination)
#            to_check = destination.seek(0)
#            to_check = destination.read()
#            print('blabla --> {}'.format(to_check))
#        check = line.replace('_IP_SERVER_', '')
#        self.assertEqual(to_check, check)
#        os.remove(myfile)

#    def test_get_ip(self):
#        dns = main.ServerDns()
#        dns.ip = '8.8.8.8'
#        self.assertEqual('8.8.8.8', dns.ip)

#    def test_get_domain_name(self):
#        dns = main.ServerDns()
#        dns.domain_name = 'coucou'
#        self.assertEqual('coucou', dns.domain_name)

#    def test_get_master(self):
#        dns = main.ServerDns()
#        dns.master = '8.8.8.8'
#        self.assertEqual('8.8.8.8', dns.master)

#    def test_get_slaves(self):
#        dns = main.ServerDns()
#        dns.slaves = '8.8.8.8'
#        self.assertEqual(['8.8.8.8'], dns.slaves)

#    def test_get_subdomain(self):
#        dns = main.ServerDns()
#        dns.subdomain = {'8.8.8.8': 'coucou'}
#        self.assertEqual({'8.8.8.8': 'coucou'}, dns.subdomain)

#    def test_get_is_master(self):
#        dns = main.ServerDns()
#        dns.ismaster = False
#        self.assertEqual(False, dns.ismaster)
