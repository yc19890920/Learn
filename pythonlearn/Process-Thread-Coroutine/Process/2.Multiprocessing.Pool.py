# -*- coding: utf-8 -*-

import multiprocessing
import time


############################################################
# 7.1) 进程池（非阻塞）

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"

# if __name__ == "__main__":
#     pool = multiprocessing.Pool(processes = 3)
#     for i in xrange(4):
#         msg = "hello %d" %(i)
#         pool.apply_async(func, (msg, ))   # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
#
#     print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
#     pool.close()
#     pool.join()   # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
#     print "Sub-process(es) done."



############################################################
# 7.2) 进程池（阻塞）

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"

# if __name__ == "__main__":
#     pool = multiprocessing.Pool(processes = 3)
#     for i in xrange(4):
#         msg = "hello %d" %(i)
#         pool.apply(func, (msg, ))   # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
#
#     print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
#     pool.close()
#     pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
#     print "Sub-process(es) done."



############################################################
# 7.3) 进程池，关注结果

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"
    return "done " + msg

# if __name__ == "__main__":
#     pool = multiprocessing.Pool(processes=4)
#     result = []
#     for i in xrange(3):
#         msg = "hello %d" %(i)
#         result.append(pool.apply_async(func, (msg, )))
#     pool.close()
#     pool.join()
#     for res in result:
#         print ":::", res.get()
#     print "Sub-process(es) done."

############################################################
# 7.4) 多个进程池

import os, random

def Lee():
    print "\nRun task Lee-%s" %(os.getpid()) #os.getpid()获取当前的进程的ID
    start = time.time()
    time.sleep(random.random() * 10) #random.random()随机生成0-1之间的小数
    end = time.time()
    print 'Task Lee, runs %0.2f seconds.' %(end - start)

def Marlon():
    print "\nRun task Marlon-%s" %(os.getpid())
    start = time.time()
    time.sleep(random.random() * 40)
    end=time.time()
    print 'Task Marlon runs %0.2f seconds.' %(end - start)

def Allen():
    print "\nRun task Allen-%s" %(os.getpid())
    start = time.time()
    time.sleep(random.random() * 30)
    end = time.time()
    print 'Task Allen runs %0.2f seconds.' %(end - start)

def Frank():
    print "\nRun task Frank-%s" %(os.getpid())
    start = time.time()
    time.sleep(random.random() * 20)
    end = time.time()
    print 'Task Frank runs %0.2f seconds.' %(end - start)

if __name__=='__main__':
    function_list=  [Lee, Marlon, Allen, Frank]
    print "parent process %s" %(os.getpid())

    pool=multiprocessing.Pool(4)
    for func in function_list:
        pool.apply_async(func)     #Pool执行函数，apply执行函数,当有一个进程执行完毕后，会添加一个新的进程到pool中

    print 'Waiting for all subprocesses done...'
    pool.close()
    pool.join()    #调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    print 'All subprocesses done.'