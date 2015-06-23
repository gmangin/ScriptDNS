# **************************************************************************** #
#                                                                              #
#                                                                              #
#    db_test.py                                                                #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/23 00:21:39 by gmangin                                   #
#    Updated: 2015/06/23 18:54:37 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

import unittest
import sys
import main
from unittest.mock import mock_open, patch


class TestFunctionFileDb(unittest.TestCase):
    def test_file_db():
        all_dns = []
        isdomain = ''
        main.file_db(all_dns, isdomain)

#    def test_get_file_db():
#        get_file_db('IP', '')
        

#    def test_init_args_parser_wrong_number(self):
#        '''Test argparse with wrong arg number'''
#        try:
#            argparse_wrong_number()
#        except SystemExit:
#            pass
#        else:
#            self.fail('Did not see exception')


if __name__ == '__main__':
    unittest.main()
