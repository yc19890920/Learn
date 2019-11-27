# -*- coding: utf-8 -*- 
"""
Author：     yangcheng
date：       2019/11/22 9:51
Description：
有时候在同一个线程中，我们可能会多次请求同一资源（就是，获取同一锁钥匙），俗称锁嵌套。
如果还是按照常规的做法，会造成死锁的。

需要注意的是，可重入锁，只在同一线程里，放松对锁钥匙的获取，其他与Lock并无二致。
"""

import threading

def main():
    global n
    # 生成可重入锁对象
    lock = threading.RLock()
    with lock:
        for i in range(1, 11):
            n += 1
            with lock:
                print(n)
                
n = 0
t1 = threading.Thread(target=main)
t2 = threading.Thread(target=main)
t1.start()
t2.start()
