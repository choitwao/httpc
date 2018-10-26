import socket
import threading
import os


class Api:

    @staticmethod
    def run(port, verbose):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(('localhost', port))
            listener.listen(1)
            print('Server is listening at ', port)
            while True:
                connection, address = listener.accept()
                request = connection.recv(1024).decode("utf-8")
                print(request)
        finally:
            listener.close()
