# coding:utf-8
import socket
from multiprocessing import Process
import re
import sys

# global constant
HTML_ROOT_DIR = "./html"
WSGI_PYTHON_DIR = "./wsgipython"


class HTTPServer(object):
    """web server class"""
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.response_headers = ""
        self.times = 0

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

    def start_response(self, status, headers):
        response_headers = "HTTP/1.1 " + status + "\r\n"
        for header in headers:
            print("*"*20 + str(self.times))
            print(header)
            print("*"*20 + str(self.times))
            self.times += 1
            response_headers += "%s: %s\r\n" % header
        self.response_headers = response_headers

    def handle_client(self, client):
        """deal with the client request"""
        request_data = client.recv(1024)
        request_lines = request_data.splitlines()
        for line in request_lines:
            print(line)
        request_start_line = request_lines[0]
        print(request_start_line.decode("utf-8"))

        file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
        method = re.match(r"(\w+) +/[^ ]* ", request_start_line.decode("utf-8")).group(1)
        # active service
        if file_name.endswith(".py"):
            try:
                # execute python file
                m = __import__(file_name[1:-3])
            except Exception:
                self.response_headers = "HTTP/1.1 404 Not Found\r\n"
                response_body = "not found"
            else:
                env = {
                    "PATH_INFO" : file_name,
                    "METHOD": method
                }
                response_body = m.application(env, self.start_response)
            response = self.response_headers + "\r\n" + response_body
        # static service
        else:
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
                response_body   = file_data.decode("utf-8")
            response = response_start_line + response_headers + "\r\n" + response_body
        print("response data: ", response)
        client.send(bytes(response, "utf-8"))
        client.close()


def main():
    print("*"*10)
    print("*"*10)
    print("*"*10)
    print("*"*10)
    print("*"*10)
    sys.path.insert(1, WSGI_PYTHON_DIR)
    http_server = HTTPServer()
    http_server.bind(7777)
    http_server.start()


if __name__ == "__main__":
    main()
