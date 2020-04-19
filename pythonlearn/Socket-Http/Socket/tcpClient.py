# -*- coding: utf-8 -*-
#
import time
import socket
import errno
import time
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# host='192.168.1.24'
host='localhost'
port=10010
address = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
s.setblocking(30)

bytes = ''
poem = 0
while True:
    try:
        # recv 方法用于TCP接收数据
        bytesread = s.recv(1024)
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

# print bytes

# import socket               # 导入 socket 模块
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
# port = 12345                # 设置端口好
#
# s.connect((host, port))
# print s.recv(1024)
# s.close()
