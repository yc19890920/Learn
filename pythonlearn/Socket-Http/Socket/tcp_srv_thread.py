# -*- coding: utf-8 -*-
#
import optparse
import os
import socket
import time
from threading import Thread
import StringIO

txt = '''1111
2222
3333
4444
'''

def server(listen_socket):
    while True:
        buf = StringIO.StringIO(txt)
        sock, addr = listen_socket.accept()
        print 'Somebody at %s wants poetry!' % (addr,)
        while True:
                try:
                    line = buf.readline().strip()
                    if not line:
                        sock.close()
                        break
                    sock.sendall(line)  # this is a blocking call
                    print 'send bytes to client:%s' % line
                    #sock.close()
                except socket.error:
                    sock.close()
                    break
                time.sleep(1)  #server和client连接后，server会故意每发送一个单词后等待一秒钟后再发送另一个单词


def main():
    ports = [10010, 10011, 10012]
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # address = ('127.0.0.1', port)
        address = ('localhost', port or 0)
        s.bind(address)    # 绑定端口
        # 2.开始监听链接
        s.listen(5)        # 等待客户端连接

        print "start listen at:%s" % (port,)
        worker = Thread(target=server, args=[s])
        worker.setDaemon(True)
        worker.start()


if __name__ == '__main__':
    main()
    while True:
        time.sleep(0.01) #如果不sleep的话,CPU会被Python完全占用了
        pass