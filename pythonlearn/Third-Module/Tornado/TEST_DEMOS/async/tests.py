# -*- coding: utf-8 -*-
#
import gevent.monkey
gevent.monkey.patch_all()

import time
import requests

def worker1():
    url = "http://192.168.1.24:8000/"
    r = requests.get(url)
    print "---------------1: {}".format(len(r.text))

def worker2():
    url = "http://192.168.1.24:8001/i2"
    r = requests.get(url)
    print "---------------2: {}".format(len(r.text))


def worker3():
    url = "http://192.168.1.24:8002/i3"
    r = requests.get(url)
    print "---------------2: {}".format(len(r.text))

def main():
    threads1 = [gevent.spawn(worker1) for i in range(100)]
    threads2 = [gevent.spawn(worker2) for i in range(100)]
    threads3 = [gevent.spawn(worker3) for i in range(100)]
    threads = []
    # threads.extend(threads1)
    # threads.extend(threads2)
    threads.extend(threads3)
    gevent.joinall(threads)


if __name__ == '__main__':
    print '------------'
    T = time.time()
    main()
    print '------------', time.time() - T

