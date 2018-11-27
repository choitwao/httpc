import argparse
import ipaddress
import socket
from udp.packet import Packet
from tcp.httpc_core.cli import Cli
from urllib.parse import urlparse
import os


# Packet Type: 1-SYN, 2-SYN-ACK, 3-ACK 4-DATA 5-ACK
class HttpcUDP:

    def __init__(self, router_host, router_port, server_host, server_port):
        self.router_host = router_host
        self.router_port = router_port
        self.server_host = server_host
        self.server_port = server_port
        self.peer_ip = ipaddress.ip_address(socket.gethostbyname(self.server_host))

    def run(self, request_line):
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Firstly handshake with the server
        is_handshaked = False
        while not is_handshaked:
            is_handshaked = self.__send_handshake__(connection)
        # If handshaked, start sending ACK+data request
        is_requested = False
        response_data = None
        retry = 0
        while not is_requested:
            retry += 1
            is_requested, response_data = self.__send_request__(connection, request_line)
        print(response_data)
        connection.close()
        return response_data

    def __send_handshake__(self, connection):
        success = False
        try:
            print('---- Handshaking ----')
            # create SYNC packet, where type = 1, seq_num = 1, payload = 'SYN'
            print('Client: Creating SYN packet')
            syn_packet = Packet(1, 1, self.peer_ip, self.server_port, 'SYN'.encode('utf-8'))
            # send the packet to the router
            print('Client: Sending SYN to router')
            connection.sendto(syn_packet.to_bytes(), (self.router_host, self.router_port))
            # set timeout to 1
            connection.settimeout(1)
            # wait for response
            print('Client: Waiting for SYN-ACK')
            response, sender = connection.recvfrom(1024)
            syn_ack_response = Packet.from_bytes(response)
            print('Client: Received packet from ', sender)
            print('Client: Received ', syn_ack_response)
            print('Client: Packet payload = ', syn_ack_response.payload.decode('utf-8'))
            # check if the packet is SYN-ACK (2)
            if syn_ack_response.packet_type == 2:
                # reset timeout
                connection.settimeout(None)
                success = True
        except socket.timeout:
            print('Client: No response after 1 second, handshake failed.')
        return success

    def __send_request__(self, connection, request_line):
        success = False
        response_data = None
        try:
            print('---- Requesting ----')
            # create ACK packet, where type = 3, seq_num = 3, payload = 'ACK'
            print('Client: Creating ACK packet')
            ack_packet = Packet(3, 3, self.peer_ip, self.server_port, request_line.encode('utf-8'))
            # send the packet to the router
            print('Client: Sending ACK to router')
            connection.sendto(ack_packet.to_bytes(), (self.router_host, self.router_port))
            # set timeout to 1
            connection.settimeout(1)
            # wait for response
            print('Client: Waiting for DATA')
            response, sender = connection.recvfrom(1024)
            data_packet = Packet.from_bytes(response)
            print('Client: Received packet from ', sender)
            print('Client: Received ', data_packet)
            print('Client: Packet payload = ', data_packet.payload.decode('utf-8'))
            # check if the packet is DATA (4)
            if data_packet.packet_type == 4:
                # reset timeout
                connection.settimeout(None)
                success = True
                response_data = data_packet.payload.decode('utf-8')
                # send ACK back
                ack_packet = Packet(5, 5, self.peer_ip, self.server_port, 'ACK'.encode('utf-8'))
                # send the packet to the router
                print('Client: Sending ACK (DATA) to router')
                connection.sendto(ack_packet.to_bytes(), (self.router_host, self.router_port))
        except socket.timeout:
            print('Client: No response after 1 second, request failed')
        return success, response_data.strip('DATA ')

    @staticmethod
    def get(url, headers):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path or '/'
        query = parsed_url.query
        request_uri = "{}?{}".format(path, query) if query else path
        req_headers = {
            'Host': host,
            'User-Agent': 'Concordia-HTTP/1.0'
        }
        if headers is not None:
            for item in headers:
                header = item.split(':')
                req_headers[header[0]] = header[1]
        request_line = "GET {} HTTP/1.0".format(request_uri)
        headers_line = ''.join('{}:{}\r\n'.format(k, v) for k, v in req_headers.items())
        request_line = '\r\n'.join((request_line, headers_line, ''))
        return request_line

    @staticmethod
    def post(url, headers, data):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path or '/'
        query = parsed_url.query
        request_uri = "{}?{}".format(path, query) if query else path
        req_headers = {
            'Host': host,
            'User-Agent': 'Concordia-HTTP/1.0',
            'Content-Length': len(data)
        }
        if headers is not None:
            for item in headers:
                header = item.split(':')
                req_headers[header[0]] = header[1]
        request_line = "POST {} HTTP/1.0".format(request_uri)
        headers_line = ''.join('{}:{}\r\n'.format(k, v) for k, v in req_headers.items())
        request_line = '\r\n'.join((request_line, headers_line, data))
        return request_line


if __name__ == '__main__':

    parser = Cli.create_parser()
    args = parser.parse_args()
    u = HttpcUDP('localhost', 3000, 'localhost', 8007)
    if args.subparser_name.upper() == 'GET':
        request_line = u.get(args.URL, args.headers)
    else:
        if args.file is not None and args.data is not None:
            print('You are not allowed to have -d and -f at the same time.')
            os._exit(1)
        if args.file is not None:
            data = ''
            with open(args.file, mode='r') as f:
                for line in f:
                    if line:
                        data += line.rstrip('\n') + '&'
            if data[-1] == '&':
                parameters = data.rstrip('&')
        elif args.data is not None:
            data = args.data
        else:
            data = ''
        request_line = u.post(args.URL, args.headers, data)
    response_data = u.run(request_line)
    if args.verbose:
        print(response_data)
    if args.output:
        with open('file/output.txt', mode='w+') as w:
            w.write(response_data)
