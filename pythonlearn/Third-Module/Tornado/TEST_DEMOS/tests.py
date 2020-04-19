# -*- coding: utf-8 -*-
#
import gevent.monkey
gevent.monkey.patch_all()

import time
import requests

def worker1():
    url = "http://192.168.1.24:8000/i1"
    r = requests.get(url)
    print "---------------1: {}".format(len(r.text))

def worker2():
    url = "http://192.168.1.24:8000/i2"
    r = requests.get(url)
    print "---------------2: {}".format(len(r.text))


def main():
    gevent.joinall([
        # gevent.spawn(worker1),
        # gevent.spawn(worker1),
        # gevent.spawn(worker1),
        # gevent.spawn(worker1),
        # gevent.spawn(worker1),

        gevent.spawn(worker2),
        gevent.spawn(worker2),
        gevent.spawn(worker2),
        gevent.spawn(worker2),
        gevent.spawn(worker2),
    ])


if __name__ == '__main__':
    T = time.time()
    main()
    print '------------', time.time() - T

