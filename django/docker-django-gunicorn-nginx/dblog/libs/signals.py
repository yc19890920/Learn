# -*- coding: utf-8 -*-
#
import signal
import gevent.signal
import functools

# 设置程序结束信号量
def init_gevent_signal(handler):
    gevent.signal(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    gevent.signal(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    gevent.signal(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

# gevent加锁
def sync_gevent_lock(sem):
    def handle_lock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sem:
                return func(*args, **kwargs)
        return wrapper
    return handle_lock
