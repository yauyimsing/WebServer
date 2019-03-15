# coding:utf-8
import socket
from  multiprocessing import Process

def handle_client(client):
    """deal with the client request"""
    # get request data from client
    request = client.recv(1024)
    print("request data: " + request.decode("utf-8"))
    # construct respond data
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: my server\r\n"
    response_body = "hello kugou"
    response = response_start_line + response_headers + "\r\n" + response_body
    print("response data:", response)
    # send response data to client
    client.send(bytes(response, "utf-8"))
    # close client
    client.close()


HTML_ROOT_DIR = ""

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("", 8000))
    server.listen(128)
    while True:
        client, client_addr = server.accept()
        print("[%s, %s]user connected" % client_addr)
        p = Process(target=handle_client, args=(client,))
        p.start()
        client.close()

if __name__ == "__main__":
    main()