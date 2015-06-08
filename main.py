# **************************************************************************** #
#                                                                              #
#                                                                              #
#    g1dns.py                                                                  #
#                                                                              #
#    By: gmangin <gaelle.mangin@hotmail.fr>                                    #
#                                                                              #
#    Created: 2015/06/02 18:44:39 by gmangin                                   #
#    Updated: 2015/06/08 13:11:51 by gmangin                                   #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/python3.4 -w

import  sys

PATH_READ="./Sample/"
PATH_WRITE="./ReadyToCopyPaste/"

FILE_OPTIONS="named.conf.options"
FILE_LOCAL="named.conf.local"
FILE_DB="db." #+domain name !

class ServerDns:
    def __init__(self):
        domain_name=''
        slaves=[]
        master=''
        subdomain=[]
        ifmaster=True

    def write_local():
        
        
def launch_subdomaine_script(domain, sub_name, sud_ip):
    with open()

def launch_dns_script():
    pass

def print_usage():
    print("""\
Usage: {} [OPTIONS]
      -add [domain name] [subdomain name] [subdomain ip]
           Add a subdomain without changing anything
           on one domain of your dns server.
      
      READ THE README
    """.format(sys.argv[0]))

def main():
    if len(sys.argv) == 1:
        launch_dns_script()
    elif len(sys.argv) == 5 and sys.argv[1] == '-add':
        launch_subdomaine_script(sys.argv[2], sys.argv[3], sys.argv[4])
    else :
        print_usage()
        
if __name__ == '__main__':
    status = main()
    sys.exit(status)

    
