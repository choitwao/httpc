import socket
import re
import threading
from ast import literal_eval
import json
import os


class Server:

    def __init__(self, port, verbose, directory):
        self.port = port
        self.verbose = verbose
        self.directory = directory

    def run(self):
        if os.path.isdir(self.directory) is False:
            os.mkdir(self.directory)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(('localhost', self.port))
        listener.listen(5)
        print('Server is listening at port ', self.port)
        connection, address = listener.accept()
        request = self.__parse_request__(connection.recv(1024).decode("utf-8"))
        while True:
            if request['method'] == 'GET':
                print('Received a GET request.')
                response = self.__get_request__(request)
            else:
                print('Received a POST request.')
                response = self.__post_request__(request)
            connection.sendall(bytes(response, "utf-8"))
            connection.close()

    def __get_request__(self, request):
        return '1'

    def __post_request__(self, request):
        return '2'

    def __parse_request__(self, request):
        print(1)
        print(request)
        request = request.split('\r\n')
        print(request)
        req = dict()
        # set method
        req['method'] = request[0].split(' ')[0]
        # set path
        if request[0].split(' ')[1] == '/':
            req['path'] = self.directory
        else:
            req['path'] = (self.directory + request[0].split(' ')[1]).replace('//', '/')
        # find and set header
        for row in request:
            if re.match('{', row):
                try:
                    req['header'] = literal_eval(row)
                except SyntaxError:
                    continue
        return req

