# **************************************************************************** #
#                                                                              #
#                                                                              #
#    class_test.py                                                             #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/19 17:13:32 by gmangin                                   #
#    Updated: 2015/06/19 19:55:33 by gmangin                                   #
#                                                                              #
# **************************************************************************** #


import unittest
import sys
import main
from unittest.mock import *

class TestClass(unittest.TestCase):
    def test_get_ip(self):
        dns = main.ServerDns()
        dns.ip = '8.8.8.8'
        self.assertEqual('8.8.8.8', dns.ip)

    def test_get_domain_name(self):
        dns = main.ServerDns()
        dns.domain_name = 'coucou'
        self.assertEqual('coucou', dns.domain_name)

    def test_get_master(self):
        dns = main.ServerDns()
        dns.master = '8.8.8.8'
        self.assertEqual('8.8.8.8', dns.master)

    def test_get_slaves(self):
        dns = main.ServerDns()
        dns.slaves = '8.8.8.8'
        self.assertEqual(['8.8.8.8'], dns.slaves)

    def test_get_subdomain(self):
        dns = main.ServerDns()
        dns.subdomain = {'8.8.8.8': 'coucou'}
        self.assertEqual({'8.8.8.8': 'coucou'}, dns.subdomain)

    def test_get_is_master(self):
        dns = main.ServerDns()
        dns.ismaster = False
        self.assertEqual(False, dns.ismaster)


if __name__ == '__main__':
    unittest.main()
