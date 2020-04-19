# -*- coding: utf-8 -*-


"""
在Python中我们主要是通过thread和threading这两个模块来实现的，
其中Python的threading模块是对thread做了一些包装的，可以更加方便的被使用，所以我们使用threading模块实现多线程编程。
一般来说，使用线程有两种模式，一种是创建线程要执行的函数，把这个函数传递进Thread对象里，让它来执行；
另一种是直接从Thread继承，创建一个新的class，把线程执行的代码放到这个新的 class里。
"""

# 1. 将函数传递进Thread对象：
import threading

def thread_fun(num):
    for n in range(0, int(num)):
        print " I come from %s, num: %s" %( threading.currentThread().getName(), n)

def main(thread_num):
    thread_list = list();
    # 先创建线程对象
    for i in range(0, thread_num):
        thread_name = "thread_%s" %i
        thread_list.append(threading.Thread(target = thread_fun, name = thread_name, args = (5,)))

    # 启动所有线程
    for thread in thread_list:
        thread.start()

    # 主线程中等待所有子线程退出
    for thread in thread_list:
        thread.join()

# 2. 继承自threading.Thread类:
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);

    def run(self):
        print "I am %s" %self.name


if __name__ == "__main__":
    main(3)

    for thread in range(0, 5):
        t = MyThread()
        t.start()