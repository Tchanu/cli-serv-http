# -*- coding: utf-8 -*-
#!/usr/bin/python
import socket
from os import fork

def init_connection():
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_address=('localhost',3000)
    sock.bind(server_address)
    sock.listen(5)
    return sock

def read_html(file_requested):
    try:
        file_handler = open("static"+file_requested,'rb')
        content = file_handler.read()
        file_handler.close()
        print ("\033[32m%s ---------------> %s:%s\033[0m" % (file_requested,addr[0],addr[1]))
        return content
    except Exception as e:
        print ("\033[31m%s(404) ---------------> %s:%s\033[0m" % (file_requested,addr[0],addr[1]))
        return read_html("/404.html")

sock=init_connection()

while True:
    print("En attente de connexions \n")
    conn, addr=sock.accept()
    pid=fork()
    if pid==0:
        sock.close()
        try:
            print ("\033[94m%s:%s connecté.\033[0m" % (addr[0],addr[1]))
            while True:
                data = conn.recv(1024)
                data_string = bytes.decode(data)
                method = data_string.split(' ')[0]

                if (method == 'GET') | (method == 'HEAD'):
                    file_requested = data_string.split(' ')[1]
                    file_requested = file_requested.split('?')[0]

                    content = read_html(file_requested)

                    conn.send(content)
        finally:
            exit()
            conn.close()
    else:
        conn.close()
