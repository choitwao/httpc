from urllib.parse import urlparse
import socket


class Request:

    @staticmethod
    def get(url, headers):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or 80
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
        request = '\r\n'.join((request_line, headers_line, ''))
        sock = socket.create_connection((host, port))
        sock.sendall(request.encode("UTF-8"))
        response_data = sock.recv(4096)
        response = response_data.decode("UTF-8")
        return response

    @staticmethod
    def post(url, headers, data):
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or 80
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
        request = '\r\n'.join((request_line, headers_line, data))
        print(request)
        sock = socket.create_connection((host, port))
        sock.sendall(request.encode("UTF-8"))
        response_data = sock.recv(4096)
        response = response_data.decode("UTF-8")
        return response


