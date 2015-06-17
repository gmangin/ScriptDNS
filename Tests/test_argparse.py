# **************************************************************************** #
#                                                                              #
#                                                                              #
#    test_argparse.py                                                          #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/17 17:33:01 by gmangin                                   #
#    Updated: 2015/06/17 17:33:03 by gmangin                                   #
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


def argparse_wrong_arg():
    args = main.init_args_parser(['-coucou'])

def argparse_wrong_number():
    args = main.init_args_parser(['-domain', 'chocolat', 'champagne'])

if __name__ == '__main__':
    unittest.main()
