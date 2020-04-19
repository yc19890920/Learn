# -*- coding: utf-8 -*-

"""
主要实现了生产者和消费者线程，双方将会围绕products来产生同步问题，首先是2个生成者生产products ，而接下来的10个消费者将会消耗products，

另外：
    Condition对象的构造函数可以接受一个Lock/RLock对象作为参数，如果没有指定，则Condition对象会在内部自行创建一个RLock；
    除了notify方法外，Condition对象还提供了notifyAll方法，可以通知waiting池中的所有线程尝试acquire内部锁。
    由于上述机制，处于waiting状态的线程只能通过notify方法唤醒，所以notifyAll的作用在于防止有线程永远处于沉默状态。
"""



import threading
import time

C = threading.Condition()
products = 0

##########################################
# 生产者
class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global products
        while True:
            if C.acquire():
                if products < 10:
                    products += 1;
                    print "Producer(%s):deliver one, now products:%s" %(self.name, products)
                    C.notify()
                else:
                    print "Producer(%s):already 10, stop deliver, now products:%s" %(self.name, products)
                    C.wait();
                C.release()
                time.sleep(2)

##########################################
# 消费者
class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global products
        while True:
            if C.acquire():
                if products > 1:
                    products -= 1
                    print "Consumer(%s):consume one, now products:%s" %(self.name, products)
                    C.notify()
                else:
                    print "Consumer(%s):only 1, stop consume, products:%s" %(self.name, products)
                    C.wait();
                C.release()
                time.sleep(2)

if __name__ == "__main__":
    for p in range(0, 2):
        p = Producer()
        p.start()

    for c in range(0, 10):
        c = Consumer()
        c.start()



"""

import threading
import time

# 商品
product = None
# 条件变量
con = threading.Condition()

# 生产者方法
def produce():
    global product
    if con.acquire():
        while True:
            if product is None:
                print 'produce...'
                product = 'anything'

                # 通知消费者，商品已经生产
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)

# 消费者方法
def consume():
    global product
    if con.acquire():
        while True:
            if product is not None:
                print 'consume...'
                product = None

                # 通知生产者，商品已经没了
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)
if __name__ == "__main__":
    t1 = threading.Thread(target=produce)
    t2 = threading.Thread(target=consume)
    t2.start()
    t1.start()

"""