from socket import SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM, socket
from multiprocessing import Process
import re

def sever_handle(new_socket, new_address):
    recv_data = new_socket.recv(1024)

    # request_start = recv_data.splitlines()[0]
    # request_start = request_start.decode("utf-8")
    # print("request_start=", request_start)
    # file_name = re.match(r"\w+ +(/.*) ", request_start).group(1)
    # print("file_name==", file_name)
    #
    # if file_name == "/":
    #     file_name = "/index.html"
    # file_path = HTML_ROOT_DIR + file_name
    # print("file_path=", file_path)
    # f = open(file_path, "r")
    # read_content = f.read()

    response_start = 'HTTP/1.1 200 OK\r\n'
    response_headers = "Content-Type: text/html;charset=utf-8\r\nMyServer: server\r\n"
    response_blank = '\r\n'
    response_body = "你好，我的小宝 ！"

    response_data = response_start + response_headers + response_blank + response_body
    print(response_data)
    new_socket.send(response_data.encode("utf-8"))
    new_socket.close()
def main():
    #创建套接字
    http_handle = socket(AF_INET, SOCK_STREAM)
    #端口重用
    http_handle.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #绑定端口
    http_handle.bind(('', 9999))
    #监听
    http_handle.listen(128)
    try:
        while True:
            #accept阻塞
            new_socket, new_address = http_handle.accept()
            print('[%s:%s]已经链接上服务器' % new_address)
            #创建进程
            Process(target=sever_handle, args=(new_socket, new_address)).start()
            new_socket.close()
    finally:
            #关闭套接字
            print('关闭套接字')
            http_handle.close()


if __name__ == '__main__':
    main()