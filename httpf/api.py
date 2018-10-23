import socket
import threading
import os

class APi:

    @staticmethod
    def httpfs(host, port, verbose, inline):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listener.bind((host, port))
            listener.listen(5)
            print('Server is listening at', port)
            while True:
                conn, addr = listener.accept()
                threading.Thread(target=handle_client, args=(conn, addr, verbose, inline)).start()
        finally:
            listener.close()

    @staticmethod
    def handle_client(conn, addr, verbose, inline):
        if verbose:
            print ('New client from', addr)
        if not inline:
            inline = '.'
        try:
            while True:
                error = False
                data = conn.recv(1024)
                if not data:
                    break
                for e in data.split("/"):
                    if e == '..':
                        error = True
                if not error:
                    reply = ""
                    if data.split(" ")[0] == "GET" and data.split(" ")[1] == "/" or data.split(" ")[1] == "":
                        if verbose:
                            print("Returning the root directory files")
                        if inline:
                            os.chdir(inline)
                            reply = filter(os.path.isfile, os.listdir(os.curdir))
                        else:
                            reply = filter(os.path.isfile, os.listdir(os.curdir))
                        reply = ', '.join(reply)
                    if data.split(" ")[0] == "GET" and data.split(" ")[1] != "/" and data.split(" ")[1] != "":
                        if verbose:
                            print("Returning the specified file contents")
                        try:
                            with open(inline + data.split(" ")[1], "r") as f:
                                reply = f.read()
                        except IOError:
                            reply = "HTTP ERROR 404"
                    if data.split(" ")[0] == "POST":
                        if verbose:
                            print("Writing to " +  data.split(" ")[1])
                        with open(inline + data.split(" ")[1], "w") as f:
                            f.write(data.split("\r\n\r\n")[1].decode("utf-8"))
                        reply = "Data successfully written to " + data.split(" ")[1]
                    reply = reply + '\n'
                    if verbose:
                        print(reply)
                    conn.sendall(reply)
                else:
                    conn.sendall("Access Denied \n")
        finally:
            conn.close()