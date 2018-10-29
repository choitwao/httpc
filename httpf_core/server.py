import socket
import calendar
import os
import datetime
import time

class Server:

    def __init__(self, port, verbose, directory):
        self.port = port
        self.verbose = verbose
        self.directory = directory
        self.mime_type = {
            'html': 'text/html',
            'txt': 'text/plain',
            'json': 'application/json',
            'xml': 'application/xml'
        }

    def run(self):
        if os.path.isdir(self.directory) is False:
            os.mkdir(self.directory)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(('localhost', self.port))
        listener.listen(5)
        print('Server is listening at port ', self.port)
        while True:
            connection, address = listener.accept()
            request = self.__parse_request__(connection.recv(1024).decode("utf-8"))
            if request['method'] == 'GET':
                print('Received a GET request.')
                response = self.__get_request__(request)
            else:
                print('Received a POST request.')
                response = self.__post_request__(request)
            connection.sendall(bytes(response, 'utf-8'))
            connection.close()

    def __get_request__(self, request):
        # handle list view
        if request['path'] == self.directory:
            if self.verbose:
                print('Returning the file list of ' + request['path'])
            if 'ACCESS' in request['headers'].keys():
                print('ACCESS header is set to ' + request['headers']['ACCESS'])
                response = ''
                for file in os.listdir(request['path']):
                    if file.split('.')[-1] == request['headers']['ACCESS']:
                        response += file + '\n'
            else:
                response = '\n'.join(os.listdir(request['path']))
            return response
        # get content of file
        elif os.path.isfile(request['path']):
            file_type = request['path'].split('/')[-1].split('.')[1]
            try:
                content_type = self.mime_type[file_type]
                print(content_type)
            except KeyError:
                content_type = None
                if self.verbose:
                    print('Unsupported file type.')
            if content_type is not None:
                with open(request['path'], 'r') as f:
                    content = f.read()
                    content_length = len(content)
                    response = self.__response_line__('200', content_type, str(content_length), content)
                    if self.verbose:
                        print('Returning the content of ' + request['path'])
            else:
                response = self.__response_line__('404', content='File type not supported.')
                if self.verbose:
                    print(request['path'] + ' is not a supported file.')
            return response
        # return no file
        else:
            print(3)
            response = self.__response_line__('404', None, content='File not found.')
            return response

    def __post_request__(self, request):
        return '2'

    def __parse_request__(self, request):
        request = request.split('\r\n')
        req = dict()
        # set method
        req['method'] = request[0].split(' ')[0]
        # set path
        if request[0].split(' ')[1] == '/':
            req['path'] = self.directory
        else:
            req['path'] = (self.directory + request[0].split(' ')[1]).replace('//', '/')
        # find and set header
        req['headers'] = dict()
        for row in request[1:]:
            if len(row.split(':')) == 2:
                req['headers'][row.split(':')[0]] = row.split(':')[1]
        return req

    def __response_line__(self, code, content_type, content_length='0', content=''):
        now = datetime.datetime.now()
        response = 'HTTP/1.1 '+ code + ' OK\nServer: Concordia - Zhipeng Cai\n'
        response += 'Date: ' + calendar.day_name[now.weekday()] + ', '
        response += str(now.day) + ' ' + calendar.month_name[now.month] + ' ' + str(now.year) + ' '
        response += str(now.time()).split('.')[0] + ' EST\n'
        if content_type is not None:
            response += 'Content-Type: ' + content_type + '\n'
            response += 'Content-length: ' + content_length + '\n'
        response += 'Connection: close\n'
        response += content
        return response

