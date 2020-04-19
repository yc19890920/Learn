# -*- coding: utf-8 -*-

import time
import socket  # 导入 socket 模块

host='localhost'
port=10010  # 设置端口
address = (host, port or 0)
delay=1
num_bytes=64
filename = 'poetry.txt'

# 1.创建套接字，绑定套接字到本地IP与端口
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)    # 绑定端口

# 2.开始监听链接
s.listen(5)   # 等待客户端连接

import threading

def accept_thrd():
    while True:
        sock, addr = s.accept()
        print u'Somebody at %s wants poetry!' % (addr,)
        fp = open(filename)
        while True:
            bytes = fp.read(num_bytes)
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


def main():
    thread_list = list();
    # 先创建线程对象
    for i in range(0, 5):
        thread_name = "thread_%s" %i
        thread_list.append(threading.Thread(target=accept_thrd, name=thread_name, args=()))

    # 启动所有线程
    for thread in thread_list:
        thread.start()

    # 主线程中等待所有子线程退出
    for thread in thread_list:
        thread.join()

main()

# while True:
#     # accept用于从已完成连接队列头返回下一个已完成连接，如果已完成连接队列为空，那么进程会被投入睡眠（套接字为阻塞方式）。
#     sock, addr = s.accept()  # 3.进入循环，不断接受客户端的链接请求  # 建立客户端连接。
#
#     print u'Somebody at %s wants poetry!' % (addr,)
#
#     fp = open(filename)
#     while True:
#         bytes = fp.read(num_bytes)
#         # fp.seek(0)
#         # bytes = fp.read()
#         if not bytes:
#             sock.close()
#             fp.close()
#             break
#
#         print u'Sending %d bytes' % len(bytes)
#
#         try:
#             # send方法用于TCP发送数据，方法签名如下：
#             sock.send(bytes)
#             # sock.sendall(bytes) # this is a blocking call  # 4.接收客户端传来的数据，并且发送给对方发送数据
#         except socket.error:
#             sock.close()
#             fp.close()
#             break
#
#         time.sleep(delay)

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

