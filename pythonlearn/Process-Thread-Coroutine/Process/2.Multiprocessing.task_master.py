# -*- coding: utf-8 -*-

import random, time, Queue
from multiprocessing.managers import BaseManager

# 发送任务的队列
task_queue = Queue.Queue()
# 接收任务的队列
result_queue = Queue.Queue()

# 把两个任务队列在网络上注册
BaseManager.register('get_task_queue',callable=lambda: task_queue)
BaseManager.register('get_result_queue',callable=lambda: result_queue)

# 绑定端口5000，设置验证码：8e8b55261098a425273f31a
manager = BaseManager(address=('',5000),authkey=b'8e8b55261098a425273f31a')

# 启动队列
manager.start()

# 获取通过网络访问的queue对象：
task = manager.get_task_queue()
result = manager.get_result_queue()

begintime = time.time()
for i in range(50):
    r = random.randint(10001,99999)
    print("Put task %d ..." % r)
    task.put(r)

for i in range(50):
    r = result.get(timeout=10)
    print("Result is %s" % r)

manager.shutdown()
print("master exit.")
endtime = time.time()
print('用时：%0.5f' %(endtime-begintime))