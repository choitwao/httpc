import sys
import os
from urlmatch import urlmatch


if __name__ == '__main__':

    command = sys.argv[1:]
    try:
        # help info
        if command[0] == 'help':
            if len(command) == 1:
                print('httpc is a curl-like application but supports HTTP protocol only.\n')
                print('Usage:\n    httpc command [arguments]\n')
                print('The commands are:\n')
                print('    get     executes a HTTP GET request and prints the response.\n')
                print('    post    executes a HTTP POST request and prints the response.\n')
                print('    help    prints this screen.\n\n')
                print('Use "httpc help [command]" for more information about a command.\n')
            elif command[1] == 'get':
                print('Usage: httpc get [-v] [-h key:value] URL\n\n')
                print('Get executes a HTTP GET request for a given URL.\n')
                print('    -v                Prints the detail of the response such as protocol, status, and headers.\n')
                print('    -h key:value      Associates headers to HTTP Request with the format\'key:value\'.\n')
            elif command[1] == 'post':
                print('Usage:  httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n\n')
                print('Post executes a HTTP POST request for a given URL with inline data or from file.\n')
                print('    -v                Prints the detail of the response such as protocol, status, and headers.\n')
                print('    -h key:value      Associates headers to HTTP Request with the format\'key:value\'.\n')
                print('    -d string         Associates an inline data to the body HTTP POST request.\n')
                print('    -h key:value      Associates the content of a file to the body HTTP POST request.\n')
                print('Either [-d] or [-f] can be used but not both.')
            else:
                print('Command error. Please use \'help\' for more info.')
        # request methods
        elif command[0] == 'get' or command[0] == 'post':
            method = command[0]
            url = command[-1]
            # check if URL exists
            match_pattern = '*://*/*'
            if urlmatch(match_pattern, command[-1]):
                request = {}
                command = command[1:-1]
                request['url'] = url
                # check if verbose
                request['verbose'] = '-v' in command
                # check if header
                if '-h' in command:
                    # validate header format
                    headerString = command[command.index('-h')+1].split(':')
                    if len(headerString) == 2:
                        header = {
                            headerString[0]: headerString[1]
                        }
                        request['header'] = header
                    else:
                        print('\'-h\' must follow by a header string in key:value format.')
                        os._exit(1)
                # GET
                if method == 'get':
                    print('get')
                    print(request)
                # POST
                else:
                    print('post')
                    print(request)
            else:
                print('Command error. URL is required and must be legit in your command.')
        else:
            print('Command error. Please use \'help\' for more info.')
    except IndexError:
        print('Command error. Please use \'help\' for more info.')

