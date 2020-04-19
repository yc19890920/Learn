# -*- coding: utf-8 -*-

import time
import socket  # 导入 socket 模块

host='localhost'
port=10010  # 设置端口
address = (host, port or 0)
delay=1
num_bytes=128
poetryfilename = 'poetry.txt'

# 1.创建套接字，绑定套接字到本地IP与端口
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)    # 绑定端口

# 2.开始监听链接
s.listen(5)   # 等待客户端连接

while True:
    # accept用于从已完成连接队列头返回下一个已完成连接，如果已完成连接队列为空，那么进程会被投入睡眠（套接字为阻塞方式）。
    sock, addr = s.accept()  # 3.进入循环，不断接受客户端的链接请求  # 建立客户端连接。

    print 'Somebody at %s wants poetry!' % (addr,)

    fp = open(poetryfilename)
    while True:
        bytes = fp.read(num_bytes)
        if not bytes:
            sock.close()
            fp.close()
            break

        print 'Sending %d bytes' % len(bytes)

        try:
            # send方法用于TCP发送数据，方法签名如下：
            sock.sendall(bytes) # this is a blocking call  # 4.接收客户端传来的数据，并且发送给对方发送数据
        except socket.error:
            sock.close()
            fp.close()
            break

        time.sleep(delay)

print 'quit'


# import socket               # 导入 socket 模块
#
# s = socket.socket()         # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
# port = 12345                # 设置端口
# s.bind((host, port))        # 绑定端口
#
# s.listen(5)                 # 等待客户端连接
# while True:
#     c, addr = s.accept()     # 建立客户端连接。
#     print '连接地址：', addr
#     c.send('欢迎访问菜鸟教程！')
#     c.close()                # 关闭连接

