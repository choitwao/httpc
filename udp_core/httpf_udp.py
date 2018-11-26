import argparse
import ipaddress
import socket
from udp_core.packet import Packet


class HttpfUDP:

    def __init__(self, server_port):
        self.server_port = server_port

    def run(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection.bind(('', self.server_port))
        print('Server is listening to ', self.server_port)
        while True:
            is_handshaked = self.handle_handshake(connection)

    def handle_handshake(self, connection):
        data, sender = connection.recvfrom(1024)
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
                # create SYN-ACK, where type = 2, seq_num = 2, payload = 'SYN-ACK'
                print('Server: Creating SYN-ACK packet')
                syn_ack_packet = Packet(2, 2, syn_packet.peer_ip_addr, syn_packet.peer_port, 'SYN-ACK'.encode('utf-8'))
                print('Server: Sending SYN-ACK to router')
                connection.sendto(syn_ack_packet.to_bytes(), sender)
                #print("Server: Waiting for ACK")
                #connection.settimeout(1)
                #response, sender = connection.recvfrom(1024)
                #ack_response = Packet.from_bytes(response)
                #print('Server: Received packet from ', sender)
                #print('Server: Received ', ack_response)
                #print('Server: Packet payload = ', ack_response.payload.decode('utf-8'))
                # check if the packet is ACK (3)
                #if ack_response.packet_type == 3:
                #    # reset timeout
                #   connection.settimeout(None)
                #    success = True
                #    data = ack_response.payload.decode('utf-8')
            except socket.timeout:
                connection.settimeout(None)
                print('Client: No response after 1 second, handshake failed.')
        return success, request_data


# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", dest='server_port', help="echo server port", type=int, default=8007)
args = parser.parse_args()
r = HttpfUDP(args.server_port)
r.run()
