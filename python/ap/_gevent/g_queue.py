# -*- coding:utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()
import gevent
from gevent.queue import Queue

message_queue = Queue()

def receiver(n):
    while not message_queue.empty():
        message = message_queue.get()
        print('Received %s  message %s' % (n, message))
        gevent.sleep(0)
    print('Quitting time!')

def sender():
    [ message_queue.put_nowait(i) for i in range(10) ]

# gevent.spawn(sender).join()

gevent.joinall([
    gevent.spawn(sender),
    gevent.spawn(receiver, 'A'),
    gevent.spawn(receiver, 'B'),
    gevent.spawn(receiver, 'C'),
    ])