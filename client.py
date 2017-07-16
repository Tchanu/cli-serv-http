# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket

class TCPClient():
    def __init__(self,interface,port):
        self.server_address=(interface, port)
        self.sock=socket.socket(socket.AF_INET, socket. SOCK_STREAM)
        self.sock.connect(self.server_address)

    def show_data(self,data,title): #function qui affiche les donnes recues
        print("\033[95m--------------------------%s----------------------\033[0m" % (title))
        print(data)
        print("\033[95m-------------------------------------------------------\033[0m" )

    def get_data(self,conn):  #recevoir des donnes depuis le serveur
        data=conn.recv(8192)
        return data.decode("utf-8")

    def run(self):
        try:
            while True:
                req=raw_input("http://localhost:3000/").encode('utf-8')
                self.sock.sendall(u'GET /'+req+' HTTP/1.1\r')
                res=self.get_data(self.sock)
                self.show_data(res,req)
        finally:
            self.sock.close()

if __name__ =='__main__':
    tcps=TCPClient('localhost',3000)
    tcps.run()
