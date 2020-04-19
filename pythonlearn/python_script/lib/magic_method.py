# -*- coding: utf-8 -*-
#
import time
import functools

# 加入多线程程序中，可以一直运行线程； 在start 启动之后
def emptyLoop():
    while 1:
        time.sleep(1)

#-----------------------------------------------------
# lock装饰器
#-----------------------------------------------------
"""
# 老式装饰器
def sync_lock(lock):
    def syncWithLock(fn):
        def newFn(*args, **kwargs):
            lock.acquire()
            try:
                return fn(*args, **kwargs)
            finally:
                lock.release()
        newFn.func_name = fn.func_name
        newFn.__doc__ = fn.__doc__
        return newFn
    return syncWithLock
"""
# 多线程加锁
def sync_lock(lock):
    def handle_lock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                lock.release()
        return wrapper
    return handle_lock

# gevent加锁 # 设定对共享资源的访问数量
def sync_gevent_lock(sem):
    def handle_lock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sem:
                return func(*args, **kwargs)
        return wrapper
    return handle_lock

