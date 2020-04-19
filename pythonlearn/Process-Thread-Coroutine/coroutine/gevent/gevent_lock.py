# -*- encoding: utf-8 -*-


import gevent.monkey
gevent.monkey.patch_all()

import gevent
import signal
import gevent.pool
from gevent.coros import Semaphore, BoundedSemaphore
import random
import traceback

import logging
import logging.handlers
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
log = logging.getLogger('gevent')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)


sem = BoundedSemaphore(1) #设定对共享资源的访问数量
glb_dict = {}
signal_stop=False

############################################################
import functools
# gevent加锁 # 设定对共享资源的访问数量
def sync_gevent_lock(sem):
    def handle_lock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sem:
                return func(*args, **kwargs)
        return wrapper
    return handle_lock

############################################################
@sync_gevent_lock(sem)
def do_worker_spawn():
    for key in glb_dict:
        log.info('do_worker_spawn start ----(%s: %i)---- semaphore' % (key, glb_dict[key]))
        gevent.sleep(1)
        log.info('do_worker_spawn finish ----(%s: %i)---- semaphore' % (key, glb_dict[key]))
    return

def worker_spawn():
    while 1:
        if signal_stop: break
        do_worker_spawn()
        gevent.sleep(2)
    return

############################################################
@sync_gevent_lock(sem)
def do_worker_pool(n):
    key = random.choice(['a', 'b', 'c'])
    log.info('do_worker_pool start -----(%i----%s)---- semaphore' % (n, key))
    if key in glb_dict:
        glb_dict[key] += 1
    else:
        glb_dict.update({
            key: 1
        })
    gevent.sleep(random.randint(1, 100)*random.choice([0.01, 0.001]))
    log.info('do_worker_pool finish -----(%i----%s)---- semaphore' % (n, key))
    return

def worker_pool():
    pool = gevent.pool.Pool(20)
    count=1
    while 1:
        if signal_stop: break
        pool.spawn(do_worker_pool, count)
        count += 1
    pool.join()
    return

############################################################
def main():
    gevent.spawn(worker_spawn)
    worker_pool()
    return

############################################################
def init():
    log.info( '--------init start---------' )
    return

def finish():
    log.info('--------finish start---------')
    do_worker_spawn()
    return

############################################################
# 设置程序结束信号量
def init_gevent_signal(handler):
    gevent.signal(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    gevent.signal(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    gevent.signal(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

# 信号量处理
def signal_handle(mode):
    log.info("catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

if __name__ == "__main__":
    log.info("program start")
    init()
    init_gevent_signal(signal_handle)
    try:
        main()
    except KeyboardInterrupt:
        log.error(traceback.format_exc())
        signal_handle('sigint')
    except:
        log.error(traceback.format_exc())
        EXIT_CODE = 1
    finally:
        finish()
    log.info("program quit")
