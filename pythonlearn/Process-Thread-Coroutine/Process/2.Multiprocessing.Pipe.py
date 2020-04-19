# -*- coding: utf-8 -*-

import multiprocessing
import time

def proc1(pipe):
    while True:
        for i in xrange(10000):
            print "send: %s" %(i)
            pipe.send(i)
            time.sleep(1)

def proc2(pipe):
    while True:
        print "proc2 rev:", pipe.recv()
        time.sleep(1)

def proc3(pipe):
    while True:
        print "PROC3 rev:", pipe.recv()
        time.sleep(1)

if __name__ == "__main__":
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc1, args=(pipe[0],))
    p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
    p3 = multiprocessing.Process(target=proc3, args=(pipe[1],))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

# proc2 rev:send: 0
#  0
# PROC3 rev:send: 1
#  1
# proc2 rev:send: 2
#  2
# PROC3 rev:send: 3
# proc2 rev: 3
# PROC3 rev:send: 4
#  4
# send: 5proc2 rev:
#  5
# send: 6
# PROC3 rev: 6
# send: 7
# proc2 rev: 7
# send: 8PROC3 rev:
#  8