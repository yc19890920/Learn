#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''socket2 进阶'''
'''
1.使用while True 实现客户端服务端循环通信
2.异常捕获处理客户端异常关闭导致的崩溃 , 针对windows系统下
3.再次添加while True 实现循环建立连接
4.客户端无消息断开连接  , 针对linux系统下
5.此处有出现断开占用问题(egon blog)  可以修改内核参数或者在绑定地址之前判断
'''
import socket

# 理解为买电话.基于ipv4 基于流式协议tcp   SOCK_DGRAM udp协议
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 注释5  重用IP地址
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# 插卡
s.bind(('127.0.0.1',10010))
# 开机  此处参数是指backlog 半连接池
s.listen(5)
while 1:
    # 等待电话接通  conn建好的连接  addr客户端地址
    conn,addr=s.accept()
    while 1:
        try:
            # 开始接收消息  此处先使用1024 每次接收的大小
            client_msg = conn.recv(1024)
            if not client_msg:
                break
            print(client_msg)
            # 将收到的消息回发回去
            conn.send(client_msg.upper())
        except BaseException as e:
            print e
            break
    # 关闭连接
    conn.close()

# 关闭手机
s.close()