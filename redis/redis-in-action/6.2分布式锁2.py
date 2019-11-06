# -*- coding:utf-8 -*-
"""
$ pip install redlock-py
python中，用Redis构建分布式锁:  https://www.jianshu.com/p/261c84ce9a6c
"""
import gevent
import uuid
import gevent.monkey
gevent.monkey.patch_all()
import time
import redis
import math
from redis.exceptions import WatchError

redis = redis.Redis(host='192.168.1.24', port=6379)
T = time.time
S = time.sleep

def acqure_lock_with_watch(redis, lockname, acquire_timeout=30, index=1):
    while 1:
        et = T() + acquire_timeout
        watch_key = 'lock:' + lockname
        p = redis.pipeline()
        while T() < et:
            try:
                p.watch(watch_key)
                # if p.exists(watch_key):
                #     print "=================1", index
                #     p.unwatch()
                #     time.sleep(1)
                #     continue
                # 开启事务
                p.multi()
                # 事务具体内容，对lockname的值进行更新
                p.set(watch_key, 1)
                p.expire(watch_key, 1200)
                time.sleep(3)
                p.execute()
                break
            except WatchError:
                # 事务运行期间，有其他客户端改变了lockname的值，抛出异常，进行重试操作
                print "=================2", index
                time.sleep(1)
                continue
        print "=================1", index
        time.sleep(2)

def acquire_lock_with_timeout(redis, lockname, acquire_timeout=10, lock_timeout=10):
    identifire = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    while 1:
        lock_timeout = int(math.ceil(lock_timeout))
        end = T() + acquire_timeout
        while T() < end:
            if redis.setnx(lockname, identifire):  # 以锁名称为键，uuid的值为值，redis服务器setnx保证了只能有一个客户端成功设置键的原子性
                redis.expire(lockname, lock_timeout)  # 设置键的过期时间，过期自动剔除，释放锁
                print identifire
            elif not redis.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
                redis.expire(lockname, lock_timeout)
            print "=================x", 1
            time.sleep(5)
            break
        print "=================x", 2

if __name__ == "__main__":
    redis.delete('lock:' + "xxxx")
    gevent.joinall([
        gevent.spawn(acqure_lock_with_watch, redis, "yyyy", 30, 3),
        gevent.spawn(acqure_lock_with_watch, redis, "xxxx", 30, 4),
        gevent.spawn(acquire_lock_with_timeout, redis, "xxxx", 30, 30),
    ])
