# coding:utf-8
import time
from FrameworkServer import HTTPServer

# global constant
HTML_ROOT_DIR = "./html"
WSGI_PYTHON_DIR = "./wsgipython"

class Application(object):
    """"""
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, start_response):
        path = env.get("PATH_INFO", "/")
        print("path: " + path)
        if path.startswith("/static"):
            file_name = path[7:]
            try:
                print("file name: " + HTML_ROOT_DIR + file_name)
                file = open(HTML_ROOT_DIR + file_name, "rb")
            except IOError:
                print("Error happens")
                status = "404 Not Found"
                headers = []
                start_response(status, headers)
                return "not found"
            else:
                file_data = file.read()
                file.close()
                status = "200 OK"
                headers = []
                start_response(status, headers)
                return file_data.decode("utf-8")
        else:
            for url, handler in self.urls:
                if path == url:
                    return handler(env, start_response)
            print("execute not found part")
            status = "404 Not Found"
            headers = []
            start_response(status, headers)
            return "not found"


def show_ctime(env, start_response):
    status = "200 OK"
    headers = {
        ("Content-Type", "text/plain")
    }
    start_response(status, headers)
    return time.ctime()


def say_hello(env, start_response):
    status = "200 OK"
    headers = {
        ("Content-Type", "text/plain")
    }
    start_response(status, headers)
    return "hello from say_hello func"


def main():
    # router list
    urls = [
        ("/", show_ctime),
        ("/ctime.py", show_ctime),
        ("/sayhello.py", say_hello)
    ]

    app = Application(urls)
    http_server = HTTPServer(app)
    http_server.bind(7777)
    http_server.start()


if __name__ == "__main__":
    main()
else:
    urls = [
        ("/", show_ctime),
        ("/ctime.py", show_ctime),
        ("/sayhello.py", say_hello)
    ]
    app = Application(urls)
