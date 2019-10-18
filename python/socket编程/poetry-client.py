# -*- coding: utf-8 -*-
#
import socket
import errno
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

HOST='localhost'
PORT=10001
RECV_BYTES = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect( (HOST, PORT) )
s.setblocking(30)

bytes = ''
poem = 0
while True:
    try:
        # recv 方法用于TCP接收数据
        bytesread = s.recv(RECV_BYTES)
        time.sleep(1)
        if not bytesread:
            break
        else:
            print bytesread
            bytes += bytesread
            s.send(b"%d"%int(time.time()))
    except socket.error, e:
        if e.args[0] == errno.EWOULDBLOCK:
            break

print bytes