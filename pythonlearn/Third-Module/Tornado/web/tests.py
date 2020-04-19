# -*- coding: utf-8 -*-
#
import gevent.monkey
gevent.monkey.patch_all()

import gevent
import gevent.pool
import time
import requests

def _sync():
    url = "http://torlearn.cn/sync"
    # url = "http://torlearn.cn/user"
    # url = "http://torlearn.cn/"
    r = requests.get(url)
    print "---------------1: {}".format(len(r.text))
    # print u"---------------1: {}".format(r.text)

def _async():
    # url = "http://torlearn.cn/async"
    url = "http://torlearn.cn/user"
    r = requests.get(url)
    print "---------------2: {}".format(len(r.text))


def sync():
    index = 200
    pool = gevent.pool.Pool(100)
    while index:
        index -= 1
        pool.spawn(_sync)
    pool.join()

def async():
    index = 200000
    pool = gevent.pool.Pool(100)
    while index:
        index -= 1
        pool.spawn(_async)
    pool.join()

def main():
    # threads = [gevent.spawn(sync) for i in range(10000)]
    # # threads = [gevent.spawn(async) for i in range(100)]
    # gevent.joinall(threads)

    # sync()
    async()


if __name__ == '__main__':
    print '------------'
    T = time.time()
    main()
    print '------------', time.time() - T

