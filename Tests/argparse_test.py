# **************************************************************************** #
#                                                                              #
#                                                                              #
#    argparse_test.py                                                          #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/18 14:11:43 by gmangin                                   #
#    Updated: 2015/06/23 01:12:44 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

import unittest
import sys
import main

class TestFunctionArgsParse(unittest.TestCase):
    def test_init_args_parser_empty(self):
        '''Test argparse empty'''
        args = main.init_args_parser('')
        check = None
        self.assertEqual(check, args.domain)

    def test_init_args_parser_domain(self):
        '''Test argparse with option -domain PATH'''
        args = main.init_args_parser(['-domain', 'PATH'])
        check = ['PATH']
        self.assertEqual(check, args.domain)

    def test_init_args_parser_wrong(self):
        '''Test argparse with wrong arg'''
        try:
            argparse_wrong_arg()
        except SystemExit:
            pass
        else:
            self.fail('Did not see exception')
            
    def test_init_args_parser_wrong_number(self):
        '''Test argparse with wrong arg number'''
        try:
            argparse_wrong_number()
        except SystemExit:
            pass
        else:
            self.fail('Did not see exception')

    def test_launch_dns_script_wrong_path(self):
        '''Test launch_dns_script with wrong path in arg option'''
        try:
            main.launch_dns_script('coucou')
        except NameError:
            pass
        else:
            self.fail('Did not see exception')

#    def test_launch_dns_script_correct_path(self):
#        '''Test launch_dns_script with a correct path in arg option'''
#        main.launch_dns_script('.')

#    def test_launch_dns_script_correct_path(self):
#        '''Go main !'''
#        main.main()


def argparse_wrong_arg():
    args = main.init_args_parser(['-coucou'])

def argparse_wrong_number():
    args = main.init_args_parser(['-domain', 'chocolat', 'champagne'])

if __name__ == '__main__':
    unittest.main()
