# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket
from os import fork


class TCPServer():
    def __init__(self,interface,port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server_address=(interface,port)
        print("Initialisation de la socket  \n ")

        self.sock.bind(self.server_address)
        self.sock.listen(5)
        self.conn = None
        print("Initialisation termine")

        self.url = None
        self.protocol = None

    def read_html(self,file_requested,client_address):
        try:
            file_handler = open("static"+file_requested,'rb')
            content = file_handler.read()
            file_handler.close()
            print ("\033[32m%s ---------------> %s:%s\033[0m" % (file_requested,client_address[0],client_address[1]))
            return content
        except Exception as e:
            print ("\033[31m%s(404) ---------------> %s:%s\033[0m" % (file_requested,client_address[0],client_address[1]))
            file_handler = open("static/404.html",'rb')
            content = file_handler.read()
            file_handler.close()
            return content

    def run(self):
        while True:
            print("En attente de connexions \n")
            self.conn,client_address = self.sock.accept()
            pid=fork()

            if pid==0:
                self.sock.close()
                try:
                    print ("\033[94m%s:%s connecté.\033[0m" % (client_address[0],client_address[1]))
                    while True:
                        data = self.conn.recv(1024)
                        data_string = bytes.decode(data)
                        method = data_string.split(' ')[0]

                        if (method == 'GET') | (method == 'HEAD'):
                            file_requested = data_string.split(' ')[1]
                            content = self.read_html(file_requested.split('?')[0],client_address)

                        self.conn.send(content)
                finally:
                    self.sock.close()
                    exit()
            else:
                self.conn.close()

if __name__ =='__main__':
    tcps=TCPServer('localhost',3000)
    tcps.run()
