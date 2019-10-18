# -*- coding: utf-8 -*-

import time
import socket

HOST='localhost'
PORT=10001
READ_BYTES = 256
delay=1
filename = 'poetry.txt'

# 1.创建套接字，绑定套接字到本地IP与端口
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind( (HOST, PORT or 0) )    # 绑定端口

# 2.开始监听链接
s.listen(5)   # 等待客户端连接

while 1:
    sock, addr = s.accept()
    print u'Somebody at %s wants poetry!' % (addr,)
    fp = open(filename)
    while 1:
        bytes = fp.read(READ_BYTES)
        if not bytes:
            sock.close()
            fp.close()
            break
        print u'Sending %d bytes' % len(bytes)
        try:
            # send方法用于TCP发送数据，方法签名如下：
            sock.send(bytes)
            bytesread = sock.recv(1024)
            print bytesread
            # sock.sendall(bytes) # this is a blocking call  # 4.接收客户端传来的数据，并且发送给对方发送数据
        except socket.error:
            sock.close()
            fp.close()
            break
        time.sleep(delay)

s.close()