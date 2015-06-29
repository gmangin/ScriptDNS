# **************************************************************************** #
#                                                                              #
#                                                                              #
#    db_test.py                                                                #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/23 00:21:39 by gmangin                                   #
#    Updated: 2015/06/28 18:17:17 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

import unittest
import sys
import os
import main
try:
        from StringIO import StringIO
except ImportError:
        from io import StringIO

class TestFunctionFileDb(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_file_db_stdout_1(self):
        '''Check file_db function with empty all_dns[]'''
        all_dns = []
        isdomain = ''
        main.file_db(all_dns, isdomain)
        out = '\n=== Getting the db file ===\n'
        self.assertEqual(sys.stdout.getvalue(), out)

    def test_file_db_stdout_2(self):
        '''Check file_db function with isdomain'''
        all_dns = full_fill_all_dns()
        isdomain = './ReadyToCopyPaste/'
        main.file_db(all_dns, isdomain)
        os.remove('./ReadyToCopyPaste/db.test1.tk')
        out = '''
=== Getting the db file ===
Writting the db file in db.test1.tk directory
'''
        self.assertEqual(sys.stdout.getvalue(), out)

    def test_file_db_stdout_3(self):
        '''Check file_db function with no isdomain'''
        all_dns = full_fill_all_dns()
        isdomain = ''
        main.file_db(all_dns, isdomain)
        os.remove('./ReadyToCopyPaste/db.test1.tk')
        out = '''
=== Getting the db file ===
Writting the db file in db.test1.tk directory
'''
        self.assertEqual(sys.stdout.getvalue(), out)

    def test_file_db(self):
        '''Check file_db function if the file is well written,
           To do that, we will compare the new file with ./Tests/DB/test.db'''
        all_dns = full_fill_all_dns()
        isdomain = '.'
        main.file_db(all_dns, isdomain)
        with open('./db.test1.tk', 'r') as test1:
                to_check = test1.read()
        with open('./Tests/DB/test.db', 'r') as test:
                check = test.read()
        self.assertMultiLineEqual(check, to_check)
        os.remove('./db.test1.tk')

    def assertMultiLineEqual(self, first, second, msg=None):
        """Assert that two multi-line strings are equal.
        If they aren't, show a nice diff.
        """
        import difflib
        self.assertTrue(isinstance(first, str),
                        'First argument is not a string')
        self.assertTrue(isinstance(second, str),
                        'Second argument is not a string')
        if first != second:
            message = ''.join(difflib.ndiff(first.splitlines(True),
                                            second.splitlines(True)))
            if msg:
                message += " : " + msg
            self.fail("Multi-line strings are unequal:\n" + message)


def full_fill_dns(domain_name, master):
    dns = main.ServerDns()
    dns.ip = '8.8.8.8'
    dns.domain_name = domain_name
    dns.master = master
    dns.slaves = '8.8.8.1'
    dns.slaves = '8.8.8.2'
    dns.slaves = '8.8.8.3'
    dns.subdomain = {'unicorn': '8.8.8.4'}
    if master == dns.ip:
        dns.is_master = True
    else:
        dns.is_master = False
    return dns


def full_fill_all_dns():
    all_dns = []
    all_dns.append(full_fill_dns('test1.tk', '8.8.8.8'))
    all_dns.append(full_fill_dns('test2.tk', '1.1.1.1'))
    return all_dns


if __name__ == '__main__':
    unittest.main()
