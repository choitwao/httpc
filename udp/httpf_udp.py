import argparse
import socket
from udp.packet import Packet
import datetime
import os
import calendar

class HttpfUDP:

    def __init__(self, server_port):
        self.server_port = server_port
        self.mime_type = {
            'html': 'text/html',
            'txt': 'text/plain',
            'json': 'application/json',
            'xml': 'application/xml'
        }

    def run(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection.bind(('', self.server_port))
        print('Server is listening to ', self.server_port)
        while True:
            # handshake with client
            is_handshaked = False
            request_data = None
            while not is_handshaked:
                is_handshaked, request_data = self.__handle_handshake__(connection)
            # handle request
            is_handled = False
            while not is_handled:
                is_handled = self.__handle_request__(connection, request_data)

    def __handle_handshake__(self, connection):
        connection.settimeout(3600)
        data, sender = connection.recvfrom(1024)
        print('---- Handshaking ----')
        success = False
        request_data = None
        # restore syn_packet that received from the client
        print('Server: Decoding SYN packet from client')
        syn_packet = Packet.from_bytes(data)
        print('Server: Received packet from ', sender)
        print('Server: Received ', syn_packet)
        print('Server: Packet payload = ', syn_packet.payload.decode('utf-8'))
        # check if the packet is SYN (1)
        if syn_packet.packet_type == 1:
            try:
                # create SYN-ACK packet, where type = 2, seq_num = 2, payload = 'SYN-ACK'
                print('Server: Creating SYN-ACK packet')
                syn_ack_packet = Packet(2, 2, syn_packet.peer_ip_addr, syn_packet.peer_port, 'SYN-ACK'.encode('utf-8'))
                print('Server: Sending SYN-ACK to router')
                connection.sendto(syn_ack_packet.to_bytes(), sender)
                print("Server: Waiting for ACK")
                connection.settimeout(3600)
                response, sender = connection.recvfrom(1024)
                ack_packet = Packet.from_bytes(response)
                print('Server: Received packet from ', sender)
                print('Server: Received ', ack_packet)
                print('Server: Packet payload = ', ack_packet.payload.decode('utf-8'))
                # check if the packet is ACK (3)
                if ack_packet.packet_type == 3:
                    # reset timeout
                    connection.settimeout(None)
                    success = True
                    request_data = {
                        'packet': ack_packet,
                        'sender': sender,
                        'peer_ip_addr': syn_packet.peer_ip_addr,
                        'peer_port': syn_packet.peer_port
                    }
            except socket.timeout:
                connection.settimeout(None)
                print('Server: No response after 1 second, handshake failed.')
        return success, request_data

    def __handle_request__(self, connection, request_data):
        # do some magic here to handle data
        print('---- Handling Request ----')
        response_data = self.__create_return__(request_data)
        sender = request_data['sender']
        success = False
        try:
            while True:
                # create DATA packet, where type = 4, seq_num = 4, payload = data
                print('Server: Creating DATA packet')
                data_packet = Packet(4, 4, request_data['peer_ip_addr'], request_data['peer_port'], response_data.encode('utf-8'))
                print('Server: Sending DATA to router')
                connection.sendto(data_packet.to_bytes(), sender)
                # wait for confirmation
                connection.settimeout(3600)
                response, sender = connection.recvfrom(1024)
                ack_packet = Packet.from_bytes(response)
                if ack_packet.packet_type != 3:
                    break
            success = True
        except socket.timeout:
            connection.settimeout(None)
            print('Client: No response after 1 second, handle request failed.')
        return success

    def __create_return__(self, request):
        request = self.__parse_request__(request['packet'].payload.decode('utf-8'))
        if request['method'] == 'GET':
            print('Received a GET request.')
            response = self.__get_request__(request)
        else:
            print('Received a POST request.')
            response = self.__post_request__(request)
        print('\n\n\n\n\n\n', response)
        return response

    def __get_request__(self, request):
        # handle list view
        if request['path'] == 'file/':
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
            except KeyError:
                content_type = None
                print('Unsupported file type.')
            if content_type is not None:
                with open(request['path'], 'r') as f:
                    content = f.read()
                    content_length = len(content)
                    response = self.__response_line__('200', content_type, str(content_length), content)
                    print('Returning the content of ' + request['path'])
            else:
                response = self.__response_line__('406', None, content='File type not supported.')
                print(request['path'] + ' is not a supported file.')
            return response
        # return no file
        else:
            print(3)
            response = self.__response_line__('404', None, content='File not found.')
            return response

    def __post_request__(self, request):
        if request['path'] == 'file/':
            response = self.__response_line__('405', None, content='Method not allowed.')
        else:
            file_type = request['path'].split('/')[-1].split('.')[1]
            try:
                content_type = self.mime_type[file_type]
            except KeyError:
                content_type = None
                print('Unsupported file type.')
            if content_type is not None:
                if not os.path.exists(request['path']):
                    os.makedirs(os.path.dirname(request['path']))
                with open(request['path'], 'w+') as f:
                    f.write(request['data'])
                response = self.__response_line__('200', content_type)
            else:
                response = self.__response_line__('406', content='File type not supported.')
                print(request['path'] + ' is not a supported file.')
        return response

    def __parse_request__(self, request):
        request = request.split('\r\n')
        req = dict()
        # set method
        req['method'] = request[0].split(' ')[0]
        # set path
        if request[0].split(' ')[1] == '/':
            req['path'] = 'file/'
        else:
            req['path'] = ('file/' + request[0].split(' ')[1]).replace('//', '/')
        # find and set header
        req['headers'] = dict()
        for row in request[1:]:
            if len(row.split(':')) == 2 and '"' not in row:
                req['headers'][row.split(':')[0]] = row.split(':')[1]
        # set data
        if req['method'] == 'POST':
            req['data'] = request[-1]
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


# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", dest='server_port', help="echo server port", type=int, default=8007)
args = parser.parse_args()
r = HttpfUDP(args.server_port)
r.run()
