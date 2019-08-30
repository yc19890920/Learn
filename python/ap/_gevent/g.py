# -*- coding: utf-8 -*-
import gevent
import gevent.monkey
import gevent.pool
gevent.monkey.patch_all()

from gevent.local import local
from gevent.event import Event, AsyncResult
from gevent.queue import Queue
from gevent.backdoor import BackdoorServer
from gevent.lock import BoundedSemaphore, Semaphore, DummySemaphore, RLock
import logging
import logging.handlers
import random
import functools

# 日志
def getLogger(name):
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
    _handler.setFormatter(logging.Formatter('%(asctime)s %(module)s %(levelname)s:%(lineno)s %(message)s'))
    log = logging.getLogger(name)
    log.addHandler(_handler)
    log.setLevel(logging.DEBUG)
    return log

#设定对共享资源的访问数量
sem = BoundedSemaphore(1)
log = getLogger(__name__)
signal_stop=False
local_stash = local()
evt = Event()
art = AsyncResult()
q = Queue()

# ------------------------------------------------------------------------
# Queue、spawn
# def init():
#     while True:
#         if signal_stop: break
#         art.set(False)
#         gevent.sleep(0.1)
#         log.info('init...')
#         art.set(True)
#         evt.set()
#         gevent.sleep(10)

def producter():
    while True:
        if signal_stop: break
        local_stash.x = 1
        x = random.random()
        y = {"y": x}
        log.info('-------1---------producter local:{}, task:{}'.format(local_stash.x, x))
        q.put(y)
        gevent.sleep(0.5)

def consumer():
    while True:
        if signal_stop: break
        local_stash.x = 2
        if not q.empty():
            task = q.get()
            log.info('-------2---------consumer local:{}, task:{}'.format(local_stash.x, task))
        gevent.sleep(1)

def consumer2():
    while True:
        if signal_stop: break
        local_stash.x = 3
        if not q.empty():
            task = q.get()
            log.info('-------3---------consumer local:{}, task:{}'.format(local_stash.x, task))
        gevent.sleep(1)

# ------------------------------------------------------------------------
# pool
def _poolworker(index):
    log.info('-------3---------poolworker index: {}'.format(index))
    gevent.sleep(10)

def poolworker():
    index = 1
    pool = gevent.pool.Pool(5)
    while 1:
        if signal_stop: break
        pool.spawn(_poolworker, index)
        index += 1

# ------------------------------------------------------------------------
# pool
# gevent加锁
def sync_gevent_lock(sem):
    def lock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sem:
                return func(*args, **kwargs)
        return wrapper
    return lock


######################################################
# 信号量处理
def signal_handle(mode):
    log.info(u"catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

# --------------信号量处理---------------
# 设置监听信号量
# 设置程序结束信号量
def register_gevent_signal(handler):
    import signal
    import gevent.signal
    gevent.signal(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    gevent.signal(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    gevent.signal(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

######################################################
def main():
    register_gevent_signal(signal_handle)
    gevent.joinall([
        # gevent.spawn(gevent.backdoor.BackdoorServer(('localhost', 6565)).serve_forever),
        gevent.spawn(poolworker),
        gevent.spawn(consumer),
        gevent.spawn(consumer2),
        gevent.spawn(producter),
    ])

if __name__ == '__main__':
    log.info("program start...")
    main()
    log.info("program end...")