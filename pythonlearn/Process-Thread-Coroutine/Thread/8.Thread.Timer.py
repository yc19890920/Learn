# -*- coding: utf-8 -*-

import time
import threading

def func():
    print 'hello timer!'
    print time.time()-t

t = time.time()
timer = threading.Timer(5, func)
timer.start()

