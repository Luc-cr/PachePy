import socket
import os
import sys

def parseHttp(text : str) -> dict:
    http = {}
    data = text.split("\n")
    if data[0] != '':
        request = data[0].split(" ")
        http['method'] = request[0]
        http['route'] = request[1]
        http['version'] = request[2]
        data.__delitem__(0)
        for i in data:
            if len(i.split(": ")) == 2:
                http[i.split(": ")[0]] = i.split(": ")[1] 
        return http
    return None

class server:
    def __init__(self, host, port, dir = "www", doc = "index.html"):
        self.host = host
        self.port = port
        self.dir = dir
        self.doc = doc
        self.status = False
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Iniciamos comunicacion TCP ip
        server.bind((host, port))
        self.server = server

    def start(self):
        self.server.listen(1)
        self.status = True
        while True:
            clientCon, clientAddr = self.server.accept()
            request = clientCon.recv(65535).decode()
            request = parseHttp(request)

            if request != None:
                if "." not in request['route']:
                    if os.path.isfile(self.dir + request['route'] +"/"+ self.doc) != True:
                        clientCon.sendall(b"HTTP/1.1 404 NOT FOUND\n\n<h1>No se encontro el recurso</h1>")
                    else:
                        file = open(self.dir + request['route'] +"/"+ self.doc)
                        clientCon.sendall(b"HTTP/1.1 200 OK\n\n"+bytes(file.read(),'utf-8'))
                elif os.path.isfile(self.dir + request['route']) != True:
                    clientCon.sendall(b"HTTP/1.1 404 NOT FOUND\n\n<h1>No se encontro el recurso</h1>")
                else:
                    file = open(self.dir + request['route'], "r")
                    clientCon.sendall(b"HTTP/1.1 200 OK\n\n"+bytes(file.read(),'utf-8'))
                    file.close()
            clientCon.close()
            if self.status == False:
                self.server.close()
                break

    def getConfig(self) -> dict:
        dic = {}
        dic['host'] = self.host
        dic['port'] = self.port
        dic['dir'] = self.dir
        return dic
