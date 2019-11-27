# -*- coding: utf-8 -*- 
"""
Author：     yangcheng
date：       2019/11/22 9:57
Description：
在编写多线程程序时，可能无意中就会写了一个死锁。
可以说，死锁的形式有多种多样，但是本质都是相同的，都是对资源不合理竞争的结果。

以本人的经验总结，死锁通常以下几种：
同一线程，嵌套获取同把锁，造成死锁。
多个线程，不按顺序同时获取多个锁。造成死锁

对于第一种，上面已经说过了，使用可重入锁。
主要是第二种。可能你还没明白，是如何死锁的。
举个例子。

  线程1，嵌套获取A,B两个锁，线程2，嵌套获取B,A两个锁。
  由于两个线程是交替执行的，是有机会遇到线程1获取到锁A，而未获取到锁B，在同一时刻，线程2获取到锁B，而未获取到锁A。
  由于锁B已经被线程2获取了，所以线程1就卡在了获取锁B处，由于是嵌套锁，线程1未获取并释放B，是不能释放锁A的，
  这是导致线程2也获取不到锁A，也卡住了。两个线程，各执一锁，各不让步。造成死锁。
  
经过数学证明，只要两个（或多个）线程获取嵌套锁时，按照固定顺序就能保证程序不会进入死锁状态。
"""

import threading
from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()

@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted( locks, key=lambda x: id( x ) )

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr( _local, 'acquired', [] )
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend( locks )
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed( locks ):
            lock.release()
        del acquired[-len( locks ):]
        

# 使用
import time
x_lock = threading.Lock()
y_lock = threading.Lock()

def thread_1():
    while True:
        with acquire(x_lock):
            with acquire(y_lock):
                print('Thread-1')
        time.sleep( 1 )
    
def thread_2():
    while True:
        with acquire(y_lock):
            with acquire(x_lock):
                print('Thread-2')
        time.sleep(1)

t1 = threading.Thread(target=thread_1)
# t1.daemon = True
t1.start()

t2 = threading.Thread(target=thread_2)
# t2.daemon = True
t2.start()


