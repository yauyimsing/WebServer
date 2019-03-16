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
    def __init__(self, application):
        """construct function, application is from framework"""
        self.app = application
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

        env = {
            "PATH_INFO" : file_name,
            "METHOD": method
        }
        response_body = self.app(env, self.start_response)
        response = self.response_headers + "\r\n" + response_body
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

    if len(sys.argv) < 2:
        sys.exit("python FrameworkServer.py Module:app")
    # python FrameworkServer.py FrameWork::app (start in shell with arguments)
    module_name, app_name = sys.argv[1].split(":")
    # module_name = "FrameWork"
    # app_name = "app"
    m = __import__(module_name)
    app = getattr(m, app_name)
    http_server = HTTPServer(app)
    http_server.bind(7777)
    http_server.start()


if __name__ == "__main__":
    main()
