# -*- coding:utf-8 -*-

def gen():
    print "hello 1"
    yield 1
    print "hello 2"
    yield 2
    print "hello 3"
    yield 3


g = gen()
x = g.next()
print x

x = g.next()
print x

x = g.next()
print x


from itertools import cycle

a = [1,2,3,4]
b = cycle(a)
import time
while True:
    print b.next()
    time.sleep(1)