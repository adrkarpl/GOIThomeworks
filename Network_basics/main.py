import json
import mimetypes
import socket
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from pathlib import Path
from threading import Thread

""" Define constants for socket configuration """


SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 5005
STORAGE_PATH = Path("storage")

""" Define HTTP request handler class """


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file(Path('./front-init').joinpath('index.html'))
        elif pr_url.path == '/message':
            self.send_html_file(Path('./front-init').joinpath('message.html'))
        else:
            if Path('./front-init').joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file(
                    Path('./front-init').joinpath('error.html'), 404)

    """ Handle POST requests """

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_udp_socket(data)
        self.send_response(HTTPStatus.FOUND.value)
        self.send_header('Location', '/')
        self.end_headers()

    """ Send an HTML file as response """

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    """ Send a static file as response """

    def send_static(self):
        file_path = f'./front-init/{self.path}'
        self.send_response(200)
        mt = mimetypes.guess_type(file_path)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())


""" Run the HTTP server """


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3003)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


""" Save data to a JSON file """


def save_data(data):
    data_parse = urllib.parse.unquote_plus(data.decode())
    data_path = STORAGE_PATH.joinpath("data.json")
    try:
        with open(data_path, encoding="utf-8") as file:
            data_json = json.load(file)
    except FileNotFoundError:
        data_json = {}
    data_json[str(datetime.now())] = {key: value for key, value in [
        el.split('=') for el in data_parse.split('&')]}
    with open(data_path, "w", encoding="utf-8") as fh:
        json.dump(data_json, fh, indent=4, ensure_ascii=False)


""" Send data to the UDP socket server """


def send_data_to_udp_socket(data):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(data, (SOCKET_IP, SOCKET_PORT))
    udp_socket.close()


""" Run the UDP socket server """


def run_udp_socket_server(ip, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    udp_socket.bind(server)
    try:
        while True:
            data, address = udp_socket.recvfrom(1024)
            save_data(data)

    except KeyboardInterrupt:
        print(f'Keyboard interrupt detected. Shutting down the server.')
    finally:
        udp_socket.close()


""" Main function """
if __name__ == '__main__':
    print('The server has been successfully started!')
    if not STORAGE_PATH.exists():
        STORAGE_PATH.mkdir()

    http_server_thread = Thread(target=run_http_server)
    http_server_thread.start()

    udp_socket_server_thread = Thread(
        target=run_udp_socket_server, args=(SOCKET_IP, SOCKET_PORT))
    udp_socket_server_thread.start()

    http_server_thread.join()
    udp_socket_server_thread.join()
