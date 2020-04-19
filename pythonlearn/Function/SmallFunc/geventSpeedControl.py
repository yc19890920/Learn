# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import gevent
import gevent.pool

import time
import random

import logging
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
log = logging.getLogger('TEST')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

def PrintNumber(num):
    log.info('num: {}'.format(num))

def main():
    pool = gevent.pool.Pool(100)
    index = 0
    __T_Time = time.time()
    while True:
        index += 1
        __T_elapsed = time.time() - __T_Time
        # 计算剩余时间
        __T_leftToWait = GLB_minInterval - __T_elapsed
        if __T_leftToWait:
            gevent.sleep(__T_leftToWait)
        pool.spawn(PrintNumber, index)
        __T_Time = time.time()
    pool.join()

def init():
    global GLB_maxSpeed, GLB_minInterval
    GLB_maxSpeed = random.randint(1, 10)
    GLB_minInterval = 1.00 / float(GLB_maxSpeed)
    log.info("Sync speed: {}, Interval: {}".format(GLB_maxSpeed, GLB_minInterval))

def speed():
    while True:
        init()
        gevent.sleep(30)

if __name__ == '__main__':
    x = [x for x in range(2000000)]
    init()
    gevent.spawn(speed)
    main()

