import argparse
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
            # handshake with client
            is_handshaked = False
            request_data = None
            while not is_handshaked:
                is_handshaked, request_data = self.handle_handshake(connection)
            # handle request
            is_handled = False
            while not is_handled:
                is_handled = self.handle_request(connection, request_data)

    def handle_handshake(self, connection):
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
                print('Client: No response after 1 second, handshake failed.')
        return success, request_data

    def handle_request(self, connection, request_data):
        # do some magic here to handle data
        print('---- Handling Request ----')
        magic_data = request_data['packet'].payload.decode('utf-8')
        magic_data_reurn = 'return data'
        sender = request_data['sender']
        success = False
        try:
            while True:
                # create DATA packet, where type = 4, seq_num = 4, payload = data
                print('Server: Creating DATA packet')
                data_packet = Packet(4, 4, request_data['peer_ip_addr'], request_data['peer_port'], magic_data_reurn.encode('utf-8'))
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


# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", dest='server_port', help="echo server port", type=int, default=8007)
args = parser.parse_args()
r = HttpfUDP(args.server_port)
r.run()
