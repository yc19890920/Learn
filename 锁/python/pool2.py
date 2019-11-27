# -*- coding: utf-8 -*- 
"""
author：     yangcheng
date：       2019/11/22 14:04
desc：

"""
import time
pool = None

# Performs a large calculation (CPU bound)
def some_work(*args):
    for i in args:
        print i
    result = None
    time.sleep(1)
    return result

# A thread that calls the above function
def some_thread():
    pool = multiprocessing.Pool( processes=3 )
    index = 0
    while True:
        r = pool.apply_async(some_work, (index,))
        index += 1
    print 'Waiting for all subprocesses done...'
    pool.close()
    pool.join()  # 调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    print 'All subprocesses done.'

# Initiaze the pool
if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()
    some_thread()