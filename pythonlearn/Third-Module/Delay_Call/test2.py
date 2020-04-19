# -*- coding: utf-8 -*-
#

import gevent.monkey
gevent.monkey.patch_all()

import gevent
import gevent.pool
import time
import traceback
from functools import partial
from gevent_delaycall import LoopingCall

def woker2(index, t):
    print '-------------------index: {}, time: {}'.format(index, time.time()-t)

def woker1(index):
    print '-------------------index: {}'.format(index)
    l = LoopingCall(3, woker2, index, time.time())
    l.start()
    # l.kill()
    return

def scan():
    index = 0
    pool = gevent.pool.Pool(10)
    while True:
        index += 1
        pool.spawn(woker1, index)
        gevent.sleep(1)
    pool.join()

# ----------------------------------
def main():
    scan()

if __name__ == "__main__":
    main()

