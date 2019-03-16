# coding:utf-8
import socket
from  multiprocessing import Process
import re

HTML_ROOT_DIR = "./html"


class HTTPServer(object):
    """web server class"""
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self, port):
        self.server.bind(("", port))

    def start(self):
        self.server.listen(128)
        while True:
            client, client_addr = self.server.accept()
            print("[%s, %s]user connected" % client_addr)
            p = Process(target=self.handle_client, args=(client,))
            p.start()
            client.close()

    @staticmethod
    def handle_client(client):
        """deal with the client request"""
        request_data = client.recv(1024)
        request_lines = request_data.splitlines()
        for line in request_lines:
            print(line)
        request_start_line = request_lines[0]
        print(request_start_line.decode("utf-8"))
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
        if file_name == "/":
            file_name = "/index.html"
        try:
            print("file name: " + HTML_ROOT_DIR + file_name)
            file = open(HTML_ROOT_DIR + file_name, "rb")
        except IOError:
            print("Error happens")
            response_start_line = "HTTP/1.1 404 Not Found\r\n"
            response_headers = "Server: my server\r\n"
            response_body = "The file is not found...ee"
        else:
            file_data = file.read()
            file.close()
            response_start_line = "HTTP/1.1 200 OK\r\n"
            response_headers = "Server: my server\r\n"
            response_body = file_data.decode("utf-8")
        response = response_start_line + response_headers + "\r\n" + response_body
        print("response data: ", response)
        client.send(bytes(response, "utf-8"))
        client.close()


def main():
    http_server = HTTPServer()
    http_server.bind(7777)
    http_server.start()


if __name__ == "__main__":
    main()
