# -*- coding: utf-8 -*-

import time

# 闭包实现资源池， 待顺序掉用
def closureSourse():
    # 从数据库或直接初始化 获取某个资源池
    S = [i for i in xrange(10, 21)]
    Ssize = len(S)

    count = [0]
    def inner():
        T = S[count[0]]
        count[0] += 1
        if count[0]==Ssize: count[0] = 0
        return T
    return inner


count = closureSourse()
print count()
print count()
# while True:
#     x = count()
#     print x
#     time.sleep(1)


## 另一种实现
from itertools import cycle
S = (i for i in xrange(10, 21))
T = cycle(S)
print T.next()
print T.next()
print T.next()
# while True:
#     x = T.next()
#     print x
#     time.sleep(1)



