import argparse
import ipaddress
import socket
from udp_core.packet import Packet

# Packet Type: 1-SYN, 2-SYN-ACK, 3-ACK 4-DATA 5-ACK
class HttpcUDP:

    def __init__(self, router_host, router_port, server_host, server_port):
        self.router_host = router_host
        self.router_port = router_port
        self.server_host = server_host
        self.server_port = server_port
        self.peer_ip = ipaddress.ip_address(socket.gethostbyname(self.server_host))

    def run(self):
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
            is_requested, response_data = self.__send_request__(connection)
        print(response_data)
        connection.close()

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

    def __send_request__(self, connection):
        success = False
        response_data = None
        try:
            print('---- Requesting ----')
            # create ACK packet, where type = 3, seq_num = 3, payload = 'ACK'
            print('Client: Creating ACK packet')
            ack_packet = Packet(3, 3, self.peer_ip, self.server_port, 'Some data'.encode('utf-8'))
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
        return success, response_data



# python echoclient.py --routerhost localhost --routerport 3000 --serverhost localhost --serverport 8007

parser = argparse.ArgumentParser()
parser.add_argument("--routerhost", dest='router_host', help="router host", default="localhost")
parser.add_argument("--routerport", dest='router_port', help="router port", type=int, default=3000)
parser.add_argument("--serverhost", dest='server_host', help="server host", default="localhost")
parser.add_argument("--serverport", dest='server_port', help="server port", type=int, default=8007)
args = parser.parse_args()

u = HttpcUDP(args.router_host, args.router_port, args.server_host, args.server_port)
u.run()
