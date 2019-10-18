# -*- coding:utf-8 -*-
"""
$ pip install redlock-py
python中，用Redis构建分布式锁:  https://www.jianshu.com/p/261c84ce9a6c
"""
from contextlib import contextmanager
from redlock import RedLock


@contextmanager
def worker_lock_manager(key, ttl, **kwargs):
    """
    分布式锁
    :param key: 分布式锁ID
    :param ttl: 分布式锁生存时间
    :param kwargs: 可选参数字典
    :return: None
    """
    redis_servers = [{
        # 'host': '127.0.0.1',
        'host': '192.168.1.24',
        'port': 6379,
        'db': 0,
        'password': ''
    }]

    rlk = RedLock(redis_servers)

    # 获取锁
    lock = rlk.lock(key, ttl)

    yield lock

    # 释放锁
    rlk.unlock(lock)

def call_lock():
    with worker_lock_manager('unique_key', 1000) as w_lock:
        if w_lock is False:
            return
        # do_something()
        print("abc")


call_lock()