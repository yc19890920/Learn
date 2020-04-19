# -*- coding: utf-8 -*-

import socket
from time import ctime

# Address and Port
HOST = ''
PORT = 8000
ADDR = (HOST, PORT)

# BufferSize
BUFFSIZE = 1024
# build socket
udpSerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind socket
udpSerSock.bind(ADDR)

try:
    while True:
        print 'waiting the message...'
        data, addr = udpSerSock.recvfrom(BUFFSIZE)
        print 'received the message: '+ data +' from: ', addr
        udpSerSock.sendto('[%s] %s' % (ctime(), data), addr)
except EOFError, KeyboardInterrupt:
    udpSerSock.close()