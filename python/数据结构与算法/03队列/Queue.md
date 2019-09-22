
Python 中的Queue实现了经典的先入先出队列，并且是线程安全的。
```
import Queue
myqueue = Queue.Queue(maxsize = 10)
Queue.Queue类即是一个队列的同步实现。队列长度可为无限或者有限。可通过Queue的构造函数的可选参数maxsize来设定队列长度。如果maxsize小于1就表示队列长度无限。
myqueue.put(10)

调用队列对象的put()方法在队尾插入一个项目。
put()有两个参数，第一个item为必需的，为插入项目的值；
第二个block为可选参数，默认为1。如果队列当前为空且block为1，put()方法就使调用线程暂停,直到空出一个数据单元。如果block为0，put方法将引发Full异常。

将一个值从队列中取出
myqueue.get()
调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。如果队列为空且block为False，队列将引发Empty异常。

python queue模块有三种队列:
1、python queue模块的FIFO队列先进先出。
2、LIFO类似于堆。即先进后出。
3、还有一种是优先级队列级别越低越先出来。 


针对这三种队列分别有三个构造函数:
1、class Queue.Queue(maxsize) FIFO 
2、class Queue.LifoQueue(maxsize) LIFO 
3、class Queue.PriorityQueue(maxsize) 优先级队列 


介绍一下此包中的常用方法:


Queue.qsize() 返回队列的大小 
Queue.empty() 如果队列为空，返回True,反之False 
Queue.full() 如果队列满了，返回True,反之False
Queue.full 与 maxsize 大小对应 
Queue.get([block[, timeout]]) 获取队列，timeout等待时间 
Queue.get_nowait() 相当Queue.get(False)
非阻塞 Queue.put(item) 写入队列，timeout等待时间 
Queue.put_nowait(item) 相当Queue.put(item, False)
Queue.task_done() 在完成一项工作之后，Queue.task_done() 函数向任务已经完成的队列发送一个信号
Queue.join() 实际上意味着等到队列为空，再执行别的操作

一些常用方法
task_done()
意味着之前入队的一个任务已经完成。由队列的消费者线程调用。每一个get()调用得到一个任务，接下来的task_done()调用告诉队列该任务已经处理完毕。
如果当前一个join()正在阻塞，它将在队列中的所有任务都处理完时恢复执行（即每一个由put()调用入队的任务都有一个对应的task_done()调用）。

join()
阻塞调用线程，直到队列中的所有任务被处理掉。
只要有数据被加入队列，未完成的任务数就会增加。当消费者线程调用task_done()（意味着有消费者取得任务并完成任务），未完成的任务数就会减少。当未完成的任务数降到0，join()解除阻塞。

put(item[, block[, timeout]])
将item放入队列中。
如果可选的参数block为True且timeout为空对象（默认的情况，阻塞调用，无超时）。
如果timeout是个正整数，阻塞调用进程最多timeout秒，如果一直无空空间可用，抛出Full异常（带超时的阻塞调用）。
如果block为False，如果有空闲空间可用将数据放入队列，否则立即抛出Full异常
其非阻塞版本为put_nowait等同于put(item, False)

get([block[, timeout]])
从队列中移除并返回一个数据。block跟timeout参数同put方法
其非阻塞方法为｀get_nowait()｀相当与get(False)

empty()
如果队列为空，返回True,反之返回False
```

# FIFO队列
```
import Queue  
q=Queue.Queue()  
for i in range(5):  
    q.put(i)  
while not q.empty():  
    print q.get(),  
输出结果为：0 1 2 3 4
```

# 后入先出LIFO队列
````
import Queue  
q=Queue.LifoQueue()  
for i in range(5):  
    q.put(i)  
  
while not q.empty():  
    print q.get(), 
输出结果为：4 3 2 1 0
````


# 优先级队列 PriorityQueue

```
import Queue  
import threading  
class Job(object):  
    def __init__(self,priority,description):  
        self.priority=priority  
        self.description=description  
        print 'New Job:',description  
        return  
    def __cmp__(self, other):  
        return cmp(self.priority,other.priority)  
q=Queue.PriorityQueue()  
q.put(Job(3,'Middle Level Job.'))  
q.put(Job(10,'Low Level Job.'))  
q.put(Job(1,'High Level Job.'))  
  
def process_job(q):  
    while True:  
        next_job=q.get()  
        print 'processing job:',next_job.description  
        q.task_done()  
workers=[threading.Thread(target=process_job,args=(q,)),  
         threading.Thread(target=process_job,args=(q,)),
         threading.Thread(target=process_job,args=(q,)),]  
for w in workers:  
    w.setDaemon(True)  
    w.start()  
q.join()  

其输出结果为：
[python] view plain copy
New Job: Middle Level Job.  
New Job: Low Level Job.  
New Job: High Level Job.  
processing job: High Level Job.  
processing job: Middle Level Job.  
processing job: Low Level Job.  

可以看到，虽然我们并没有按照priority的顺序将对象压入队列，但是队列的排序还是按照priority输出的，这就是因为我们使用了PriorityQueue对象。
```
