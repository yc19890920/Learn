# -*- coding: utf-8 -*-

import socket

# Address and Port 
HOST = 'localhost'
PORT = 8000
ADDR = (HOST, PORT)

# BufferSize
BUFSIZ = 1024

# build socket 
udpCliSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = raw_input('> ')
    udpCliSock.sendto(data, ADDR)
    data = udpCliSock.recvfrom(BUFSIZ)
    if not data:
        break
    print data
udpCliSock.close()