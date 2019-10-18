# -*- coding: utf-8 -*-

import socket
import time
import traceback
from threading import Thread

def server(sock):
    while 1:
        conn, addr = sock.accept()
        print 'Somebody at %s wants poetry!' % (addr, )
        fp = open('poetry.txt')
        while 1:
            bytes = fp.read(1024)
            if not bytes:
                break
            try:
                # send方法用于TCP发送数据，方法签名如下：
                conn.send(bytes)
                print 'send bytes to client:%s' % bytes
                # bytesread = sock.recv(1024)
                # # 4.接收客户端传来的数据，并且发送给对方发送数据
                # sock.sendall(bytes) # this is a blocking call
            except socket.error:
                print traceback.format_exc()
                break
        conn.close()
        fp.close()

def run():
    ports = [10002, 10003, 10004]
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # address = ('127.0.0.1', port)
        address = ('localhost', port or 0)
        s.bind(address)  # 绑定端口
        # 2.开始监听链接
        s.listen(5)  # 等待客户端连接

        print "start listen at:%s" % (port,)
        worker = Thread(target=server, args=[s])
        worker.setDaemon(True)
        worker.start()

def sleep():
    while 1:
        time.sleep(5)

if __name__ == "__main__":
    run()
    sleep()
