#!/usr/bin/env python
# -*- coding:utf-8 -*-
''''''
'''
1.使用while True 实现客户端服务端循环通信
2.if not msg:continue  判断是否有消息 防止空消息问题
'''
import socket
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #等同于服务端
s.connect(('127.0.0.1', 10002))     #拨通电话 注意此处是一个元组的形式

while True:
    msg = raw_input('input message>>:').strip()
    if not msg:
        continue
    s.send(msg)
    print msg
    # 转为二进制发出去
    # s.send(msg.encode('utf-8'))
    print('ready to recv message')

    backmsg = s.recv(2048)
    # while 1:
    #     # 接收消息
    #     _backmsg = s.recv(64)
    #     if not _backmsg:
    #         break
    #     backmsg += backmsg

    j = json.loads(backmsg)
    print j
    if j['quit']:
        break
    s.send(b'xxx')
    # print(backmsg.decode('utf-8'))

s.close()