import argparse
import ipaddress
import socket
from udp_core.packet import Packet


class HttpcUDP:

    def __init__(self, router_host, router_port, server_host, server_port):
        self.router_host = router_host
        self.router_port = router_port
        self.server_host = server_host
        self.server_port = server_port

    def run(self):
        peer_ip = ipaddress.ip_address(socket.gethostbyname(self.server_host))
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Firstly handshake with the server
        is_handshaked = False
        while not is_handshaked:
            is_handshaked = self.send_handshake(connection, peer_ip)
        # If handshaked, start sending ACK+data request
        connection.close()

    def send_handshake(self, connection, peer_ip):
        success = False
        try:
            # create sync packet, where type = 1, seq_num = 1, payload = 'SYN'
            print('Client: Creating SYN packet')
            syn_packet = Packet(1, 1, peer_ip, self.server_port, 'SYN'.encode('utf-8'))
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

# python echoclient.py --routerhost localhost --routerport 3000 --serverhost localhost --serverport 8007

parser = argparse.ArgumentParser()
parser.add_argument("--routerhost", dest='router_host', help="router host", default="localhost")
parser.add_argument("--routerport", dest='router_port', help="router port", type=int, default=3000)
parser.add_argument("--serverhost", dest='server_host', help="server host", default="localhost")
parser.add_argument("--serverport", dest='server_port', help="server port", type=int, default=8007)
args = parser.parse_args()

u = HttpcUDP(args.router_host, args.router_port, args.server_host, args.server_port)
u.run()
