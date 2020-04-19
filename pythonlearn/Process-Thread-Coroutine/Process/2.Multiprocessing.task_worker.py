# -*- coding: utf-8 -*-

import time, sys, Queue
from multiprocessing.managers import BaseManager

# 获取网络中的Queue,并注册
BaseManager.register('get_task_queue')
BaseManager.register('get_result_queue')

# 连接到manager.py所在机器 server_addr 为远程master服务器的ip地址
server_addr = '127.0.0.1'
print("Connecting to server %s" % server_addr)
m = BaseManager(address=(server_addr, 5000),authkey=b'8e8b55261098a425273f31a')
m.connect()

#获取Queue对象
task = m.get_task_queue()
result = m.get_result_queue()

#从task中获取任务，并把结果写入result队列

for i in range(50):
    try:
        n = task.get(timeout=2)
        print('run task %d * %d' %(n,n))
        r = '%d * %d = %d ' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('Task queue is empty')
#处理结束
print('Worker exit .')