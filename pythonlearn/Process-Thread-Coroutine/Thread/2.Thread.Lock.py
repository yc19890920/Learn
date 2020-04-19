# -*- coding: utf-8 -*-

import threading
import time

counter = 0
mutex = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global counter
        time.sleep(1);
        with mutex:
            counter += 1
            print "I am %s, set counter:%s" % (self.name, counter)

if __name__ == "__main__":
    for i in range(0, 200):
        my_thread = MyThread()
        my_thread.start()