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


    def get_file(self,request):#read html file.
        self.accepted_filetypes(request)
        try:
            file_handler = open("static"+request,'rb')
            content = file_handler.read()
            file_handler.close()
            self.print_http_status(request,'200',self.client_addr[0],self.client_addr[1])
            return content
        except Exception as e:#404
            return self.get_error(request,"404")


    def get_error(self,request,error):#return errors to client
        self.print_http_status(request,error,self.client_addr[0],self.client_addr[1])
        file_handler = open("static/"+error+".html",'rb')
        content = file_handler.read()
        file_handler.close()
        return content


    def print_http_status(self,request,status,client_ip,client_port):
        color = '32'
        if(status != '200'):
            color = '31'
        print ("\033[%sm%s(%s) ---------------> %s:%s\033[0m" % (color,request,status,client_ip,client_port))


    def accepted_filetypes(self,file):
        afps = ['html','jpg','gif']
        filetype = file.split(".")[-1]
        for afp in afps:
            if(afp == filetype):
                return True
        return False


    def accepted_methods(self,method):
        return method == "GET"#only GET is supported right now


    def accepted_http_version(self,version):


    def is_valid_request(self,hostname):#checking request
        allowed = re.compile(r"/(?!-)[//,\.,a-z0-9-]{1,63}$", re.IGNORECASE)
        return allowed.match(hostname) != None


    def http_req(self):#process http request
        data = bytes.decode(self.conn.recv(1024))
        method = data.split(' ')[0]
        request = data.split(' ')[1]

        if (request == '/'):#homepage
            request = '/index.html'

        if (self.accepted_http_version(data.split(' ')[2]) == False):#HTTP Version Not Supported
            return self.get_error(request,"505")

        if(self.accepted_methods(method) == False):#unsupported method
            return self.get_error(request,"405")

        if(self.is_valid_request(request) == False):#invalid request
            return self.get_error(request,"400")

        if(self.accepted_filetypes(request) == False):#unsuported media
            return self.get_error(request,"415")

        return self.get_file(request.split('?')[0])#everything ok


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
