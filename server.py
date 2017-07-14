# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket
import re
from os import fork


class TCPServer():
    def __init__(self,interface,port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server_address=(interface,port)
        print("Initialisation de la socket  \n ")

        self.sock.bind(self.server_address)
        self.sock.listen(5)
        print("Initialisation termine")


    def get_html(self,file_requested):
        try:
            file_handler = open("static"+file_requested,'rb')
            content = file_handler.read()
            file_handler.close()
            print ("\033[32m%s ---------------> %s:%s\033[0m" % (file_requested,self.client_addr[0],self.client_addr[1]))
            return content
        except Exception as e:#404
            print ("\033[31m%s(404) ---------------> %s:%s\033[0m" % (file_requested,self.client_addr[0],self.client_addr[1]))
            file_handler = open("static/404.html",'rb')
            content = file_handler.read()
            file_handler.close()
            return content
    def is_valid_request(self,hostname):
        allowed = re.compile(r"/(?!-)[//,\.,a-z0-9-]{1,63}$", re.IGNORECASE)
        return allowed.match(hostname) != None

    def http_req(self):
        data = self.conn.recv(1024)
        data = bytes.decode(data)
        method = data.split(' ')[0]

        if (method == 'GET') | (method == 'HEAD') | (method == 'PUT'):#supported methods
            file_requested = data.split(' ')[1]
            if(self.is_valid_request(file_requested)):
                content = self.get_html(file_requested.split('?')[0])#everything ok
            else:
                content = self.get_html("/400.html")            

        else:
            content = self.get_html("/405.html")
        return content

    def run(self):
        while True:
            print("En attente de connexions \n")
            self.conn,self.client_addr = self.sock.accept()
            pid=fork()

            if pid==0:
                self.sock.close()
                try:
                    print ("\033[94m%s:%s connecté.\033[0m" % (self.client_addr[0],self.client_addr[1]))
                    while True:
                        content = self.http_req()#HTTP request
                        self.conn.send(content)#Send content
                except Exception as e:
                    print(e)
                finally:
                    self.sock.close()
                    exit()
            else:
                self.conn.close()

if __name__ =='__main__':
    tcps=TCPServer('localhost',3000)
    tcps.run()
