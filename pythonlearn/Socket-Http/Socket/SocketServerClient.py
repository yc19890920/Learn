# -*- coding:utf-8 -*-

import socket

# Address and Port
HOST = '127.0.0.1'
PORT = 10010
ADDR = (HOST, PORT)

# BufferSize
BUFSIZ = 1024

while True:
    # note: SocketServer 的请求处理器的默认行为是接受连接，
    # 得到请求，然后就关闭连接，所以需要多次连接
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)

    # process data
    data = raw_input('> ')
    # data = '123'
    if not data:
        break
    tcpCliSock.send('%s\r\n' % data)

    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print data.strip()
    tcpCliSock.close()