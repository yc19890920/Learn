#!/usr/bin/env python
#coding:utf8

'''
 服务器的实现 采用select的方式
'''

import select
import socket
import sys
import Queue

#创建套接字并设置该套接字为非阻塞模式
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(0)

#绑定套接字
server_address = ('localhost',10010)
print >>sys.stderr,'starting up on %s port %s'% server_address
server.bind(server_address)

#将该socket变成服务模式
#backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
#这个值不能无限大，因为要在内核中维护连接队列
server.listen(5)


#初始化读取数据的监听列表,最开始时希望从server这个套接字上读取数据
inputs = [server]


#初始化写入数据的监听列表，最开始并没有客户端连接进来，所以列表为空
outputs = []

#要发往客户端的数据
message_queues = {}
while inputs:
    print >>sys.stderr,'waiting for the next event'
    #调用select监听所有监听列表中的套接字，并将准备好的套接字加入到对应的列表中
    readable, writable, exceptional = select.select(inputs, outputs, inputs) #列表中的socket 套接字  如果是文件呢？
    #监控文件句柄有某一处发生了变化 可写 可读  异常属于Linux中的网络编程
    #属于同步I/O操作，属于I/O复用模型的一种
    #rlist--等待到准备好读
    #wlist--等待到准备好写
    #xlist--等待到一种异常
    #处理可读取的套接字

    '''
        如果server这个套接字可读，则说明有新链接到来
        此时在server套接字上调用accept,生成一个与客户端通讯的套接字
        并将与客户端通讯的套接字加入inputs列表，下一次可以通过select检查连接是否可读
        然后在发往客户端的缓冲中加入一项，键名为:与客户端通讯的套接字，键值为空队列
        select系统调用是用来让我们的程序监视多个文件句柄(file descrīptor)的状态变化的。程序会停在select这里等待，
        直到被监视的文件句柄有某一个或多个发生了状态改变
        '''


    '''
        若可读的套接字不是server套接字,有两种情况:一种是有数据到来，另一种是链接断开
        如果有数据到来,先接收数据,然后将收到的数据填入往客户端的缓存区中的对应位置，最后
        将于客户端通讯的套接字加入到写数据的监听列表:
        如果套接字可读.但没有接收到数据，则说明客户端已经断开。这时需要关闭与客户端连接的套接字
        进行资源清理
        '''
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print >>sys.stderr,'connection from',client_address
            connection.setblocking(0)#设置非阻塞
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print >>sys.stderr,'received "%s" from %s'% (data, s.getpeername())
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print >>sys.stderr,'closing',client_address
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    #处理可写的套接字
    '''
        在发送缓冲区中取出响应的数据，发往客户端。
        如果没有数据需要写，则将套接字从发送队列中移除，select中不再监视
        '''
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()

        except Queue.Empty:
            print >>sys.stderr,'  ', s.getpeername(),'queue empty'
            outputs.remove(s)
        else:
            print >>sys.stderr,'sending "%s" to %s'% \
                               (next_msg,s.getpeername())
            s.send(next_msg)



    # 处理异常情况
    for s in exceptional:
        for s in exceptional:
            print >>sys.stderr,'exception condition on',s.getpeername()
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
