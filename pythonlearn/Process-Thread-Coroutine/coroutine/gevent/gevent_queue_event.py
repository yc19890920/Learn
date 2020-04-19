# -*- coding: utf-8 -*-
#

import gevent.monkey
gevent.monkey.patch_all()

import gevent
import gevent.pool
import gevent.queue
import gevent.event
import json
import random
import redis

from lib import queue

import logging
import logging.handlers
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
log = logging.getLogger('gevent')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)


redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.StrictRedis(connection_pool=redis_pool)

evt = gevent.event.Event()
pool = gevent.pool.Pool(5)
retry = queue.RetryQueue()
channel = gevent.queue.Channel()

# d = {
#     'name': '20170726-2369-12',
#     'result': [
#         {'return_code': -1},
#         {'return_code': 2},
#         {'return_code': 3},
#     ]
# }
############################################################

def setter():
    '''After 3 seconds, wake all threads waiting on the value of evt'''
    print('A: Hey wait for me, I have to do something')
    gevent.sleep(3)
    print("Ok, I'm done")
    evt.set()

def do_worker(count, name="A"):
    '''After 3 seconds the get call will unblock'''
    print("I'll wait for you, %s %d" % (name, count))
    evt.wait()  # blocking
    print("It's about time, %s %d" % (name, count))

def waiter(name="A"):
    '''After 3 seconds the get call will unblock'''
    # print("I'll wait for you, %s" % name)
    # evt.wait()  # blocking
    # print("It's about time, %s" % name)

    count = 0
    while count < 5:
        count += 1
        pool.spawn(do_worker, count, name)
    pool.join()
    return

############################################################
def writer():
    count = 1
    while True:
        count += 1
        channel.put(count)
        gevent.sleep(1)
    return

def reader():
    while True:
        d = channel.get()
        log.info('channel count:%d' % d)



############################################################
def retry_put_routine():
    for ident in reversed(redis.lrange('retry_waiting', 0, -1)):
        d = json.loads(redis.hget('detail', ident))
        retry.put(d['result'][-1]['deliver_time'] + 1800, d)
    while True:
        ident = redis.brpoplpush('retry_waiting_temp', 'retry_waiting')
        d = json.loads(redis.hget('detail', ident))
        retry.put(d['result'][-1]['deliver_time'] + 1800, d)

def retry_routine():
    while True:
        d = retry.get()
        (
            redis.pipeline()
                .lpush('received', d['mail_ident'])
                .lrem('retry_waiting', 0, d['mail_ident'])
                .execute()
        )

############################################################
def main():
    gevent.joinall([
        # gevent.spawn(writer),
        # gevent.spawn(reader),

        gevent.spawn(retry_routine),
        gevent.spawn(retry_put_routine),


        gevent.spawn(setter),
        gevent.spawn(waiter, "A"),
        gevent.spawn(waiter, "B"),
        gevent.spawn(waiter, "C"),
        gevent.spawn(waiter, "D"),
        gevent.spawn(waiter, "E")
    ])

if __name__ == "__main__":
    main()