# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket

def show_data(data,title): #function qui affiche les donnes recues
    print("\033[95m--------------------------%s----------------------\033[0m" % (req))
    print(data)
    print("\033[95m-------------------------------------------------------\033[0m" )

def get_data(conn):  #recevoir des donnes depuis le serveur
    data=conn.recv(8192)
    return data.decode("utf-8")    

server_address=('localhost', 3000)

sock=socket.socket(socket.AF_INET, socket. SOCK_STREAM)
sock.connect(server_address)

try:
    while True:        
        req=raw_input("http://localhost:3000/").encode('utf-8')     
        rv=sock.sendall(u'GET /'+req+' HTTP/1.1\r')
        res=get_data(sock)
        show_data(res,req)        
finally:
    sock.close()
