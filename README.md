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

## Just add a subdomain

* you won't need the conf, just launch the script with the option -add :
> python3.4 main.py -add [domain name] [subdomain name] [subdomain ip]

* you just have to precise to which domain you want to add the subdomain. And subdomain name and ip ofcourse.

* There is log in order to check if everything went well :)

# CMD BASIC

* in order to deploy a dns server (don't forget to fullfill the conf file)

> python3.4 main.py

* in order to add a subdomain to any domain on your server.

> python3.4 main.py -add [domain name] [subdomain name] [subdomain ip]

# Have Fun !