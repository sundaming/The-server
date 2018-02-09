from socket import socket, AF_INET, SO_REUSEADDR, SOL_SOCKET, SOCK_STREAM
from multiprocessing import Process
import re
HTML_ROOT_DIR = "./html"
def handle_client(new_socket, new_address):
   recv_data = new_socket.recv(1024)
   request_start = recv_data.splitlines()[0]
   request_start = request_start.decode("utf-8")
   print("request_start=", request_start)
   file_name = re.match(r"\w+ +(/.*) ", request_start).group(1)
   print("file_name==", file_name)

   if file_name != "/":
      file_path = HTML_ROOT_DIR + file_name
      print("file_path==", file_path)
      try:
         f = open(file_path, "r")
      except :
         response_start = "HTTP/1.1 404 Not Found File!\r\n"
         response_headers = "Content-Type: text/html;charset=utf-8\r\nMyServer: hahah\r\n"
         response_blank = "\r\n"
         response_body = open("./html/404.html", "r").read()
      else:
         response_start = "HTTP/1.1 200 OK\r\n"
         response_headers = "Content-Type: text/html;charset=utf-8\r\nMyServer: hahah\r\n"
         response_blank = "\r\n"
         response_body = f.read()

   else:
      #http://127.0.0.1:8888/
      print(recv_data)
      response_start = "HTTP/1.1 200 OK\r\n"
      response_headers = "Content-Type: text/html;charset=utf-8\r\nMyServer: hahah\r\n"
      response_blank = "\r\n"
      response_body = """你好，我的小宝贝!"""
   response_data = response_start + response_headers + response_blank + response_body
   print("response_data==",response_data)
   new_socket.send(response_data.encode("utf-8"))
   new_socket.close()

def main():
   http_server = socket(AF_INET,SOCK_STREAM)
   http_server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
   http_server.bind(("", 9999))
   http_server.listen(128)
   try:
      while True:
         # accept
         new_socket,new_address = http_server.accept()
         print("[%s:%s]已经链接到服务器" % new_address)
         Process(target=handle_client,args=(new_socket,new_address)).start()
         new_socket.close()
   finally:
      print("关闭最外边070的套接字")
      http_server.close()

if __name__ == "__main__":
   main()