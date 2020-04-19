# -*- coding: utf-8 -*-
#

from gevent import monkey
monkey.patch_all()

import random
import gevent
import gevent.pool

import logging
import logging.handlers
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
log = logging.getLogger('gevent')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

############################################################
def init():
    log.info('start init...')
    log.info('finish init...')
    return

def finish():
    return


############################################################
def do_worker_1(count):
    log.info('do_worker_1, count={}'.format(count))
    gevent.sleep(random.random()*10)
    return

def worker_1():
    log.info('start worker_1...')
    pool = gevent.pool.Pool(5)
    count = 20
    while count:
        count -= 1
        pool.spawn(do_worker_1, count)
    pool.join()
    log.info('finish worker_1...')
    return


############################################################
def worker_2():
    log.info('start worker_2...')
    log.info('finish worker_2...')
    return

############################################################
def do_worker_3(count):
    log.info('do_worker_3, count={}'.format(count))
    gevent.sleep(random.random()*10)
    return

def worker_3():
    log.info('start worker_3...')
    pool = gevent.pool.Pool(5)
    while True:
        pool.spawn(do_worker_3, random.randint(1,100000))
    pool.join()
    log.info('finish worker_3...')
    return


############################################################
def main():
    init()
    gevent.joinall([
        gevent.spawn(worker_1),
        gevent.spawn(worker_2),
        gevent.spawn(worker_3),
    ])

if __name__ == "__main__":
    main()
