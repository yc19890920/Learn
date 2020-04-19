# -*- coding:utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()

import gevent
import gevent.pool

import requests

def _test():
    r = requests.get("http://192.168.1.24:8888/")
    print r.text
    # gevent.sleep(1)

def test():
    pool = gevent.pool.Pool(20)
    while True:
        pool.spawn(_test)
    pool.join()


if __name__ == "__main__":
    test()
