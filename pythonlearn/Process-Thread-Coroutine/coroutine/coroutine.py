# -*- coding:utf-8 -*-

"这是一个用协程实现的一个典型的生产者-消费者模型."

def consumer():
    n = 0
    print "consumer init"
    while True:
        # print n
        n = yield n
        print '---------', n
        if not n:
            raise Exception('no production')
        n -= 1
        print "consuption 1,left %d" % n

def produce(c):
    n = 0
    # next(c)
    c.next()
    while n < 6:
        n +=2
        print "produce 2,left %d" % n
        n = c.send(n)
        print "left %d" % n
    c.close()

c = consumer()
produce(c)