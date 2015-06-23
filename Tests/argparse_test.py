# **************************************************************************** #
#                                                                              #
#                                                                              #
#    argparse_test.py                                                          #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/18 14:11:43 by gmangin                                   #
#    Updated: 2015/06/23 23:06:26 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

import unittest
import sys
import main

class TestFunctionArgsParse(unittest.TestCase):
    def test_init_args_parser_empty(self):
        '''Test argparse empty'''
        args = main.init_args_parser('')
        check = ''
        self.assertEqual(check, args)

    def test_init_args_parser_domain(self):
        '''Test argparse with option -domain PATH'''
        args = main.init_args_parser(['-domain', '.'])
        check = '.'
        self.assertEqual(check, args)

    def test_init_args_parser_wrong(self):
        '''Test argparse with wrong arg'''
        try:
            main.init_args_parser(['-coucou'])
        except SystemExit:
            pass
        else:
            self.fail('Did not see exception')
            
    def test_init_args_parser_wrong_number(self):
        '''Test argparse with wrong arg number'''
        try:
            main.init_args_parser(['-domain', 'chocolat', 'champagne'])
        except SystemExit:
            pass
        else:
            self.fail('Did not see exception')

    def test_launch_dns_script_wrong_path1(self):
        '''Test launch_dns_script with wrong path in arg option'''
        try:
            main.init_args_parser(['-domain', 'coucou'])
        except NameError:
            pass
        else:
            self.fail('Did not see exception')

# NEED TO BE DONE !!!
#    def test_launch_dns_script_no_domain(self):
#        main.launch_dns_script('')

#    def test_launch_dns_script_domain(self):
#        main.launch_dns_script('.')

#    def test_main(self):
#        pass


if __name__ == '__main__':
    unittest.main()
