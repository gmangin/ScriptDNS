PATH_READ="./Sample/"
PATH_WRITE="./ReadyToCopyPaste/"

FILE_OPTIONS="named.conf.options"
FILE_LOCAL="named.conf.local"
FILE_DB="db." #+domain name !

if __name__ == '__main__':
    file_to_read = PATH_READ + FILE_OPTIONS
    file_to_write = PATH_WRITE + FILE_OPTIONS 
    with open(file_to_read, 'r') as to_read:
        with open(file_to_write, 'w') as to_write:
            for line in to_read:
                print(to_write.write(line))
    print('coucou')
