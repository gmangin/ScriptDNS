```
####################################################################
##                                                                ##
##   ____  _____ ______     _______ ____      ____  _   _ ____    ##
##  / ___|| ____|  _ \ \   / / ____|  _ \    |  _ \| \ | / ___|   ##
##  \___ \|  _| | |_) \ \ / /|  _| | |_) |   | | | |  \| \___ \   ##
##   ___) | |___|  _ < \ V / | |___|  _ <    | |_| | |\  |___) |  ##
##  |____/|_____|_| \_\ \_/  |_____|_| \_\   |____/|_| \_|____/   ##
##                                                                ##
##                                                                ##
####################################################################
```

# Server DNS Description

# Installation Basic

YOU NEED A DOMAIN NAME AND A SERVER

* On the master server, install bind9
> sudo apt-get install bind9

## DNS Script to deploy an server dns

* Full fill the conf file with all what you need
(it depends if you have slave(s) server(s) and subdomain(s), you might won 't need everything)

* Then launch the script.

* There is log in order to check if everything went well :)

## Option root not set yet

# CMD BASIC

* in order to deploy a dns server (don't forget to fullfill the conf file)

> python3 main.py

# Unit Tests

* in order to deploy unit test :

> python3 test.py

* or even better : 

> python3 -m unittest discover


# Have Fun !
