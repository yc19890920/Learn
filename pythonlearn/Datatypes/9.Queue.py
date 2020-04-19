# coding: utf-8

import Queue
import threading
import time
import itertools
import random
import sys
import traceback

signal_stop=False

import signal

############################################################
# 信号量处理
def signal_handle(signum, frame):
    print "catch signal: %s"% signum
    global signal_stop
    signal_stop = True

def init_signal(handler_exit):
    signal.signal(signal.SIGINT, handler_exit)  # 处理 Ctrl-C
    signal.signal(signal.SIGTERM, handler_exit)  # 处理 kill
    signal.signal(signal.SIGCHLD, handler_exit)  # 处理 signal.alarm()

init_signal(signal_handle)

############################################################
class ConsumerThread(threading.Thread):
    '消费者'

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue=queue

    def run(self):
        print 'I am Consumer Thread'
        while True:
            counter=self.queue.get()
            print 'Going to Sleep ( %d ) ' % counter
            time.sleep(random.randint(1, 100) * 0.01)
            print ' I am up ( %d )!' % counter
            self.queue.task_done()
            time.sleep(1)


############################################################
def producerLoop(queue):
    '生产者'
    _next = itertools.cycle(xrange(100))
    while 1:
        if signal_stop: break
        queue.put(_next.next())
        time.sleep(0.1)
    queue.join()


############################################################
def main():
    _threads = []
    queue = Queue.Queue(50)
    for i in range(10):
        _threads.append(ConsumerThread(queue))

    for worker in _threads:
        print 'Going to Thread!'
        worker.daemon=True
        worker.start()

    producerLoop(queue)
    return

if __name__ == "__main__":
    print u'program start...'
    EXIT_CODE=0
    try:
        main()
    except:
        print traceback.format_exc()
        EXIT_CODE = 1
    print u"program quit..."
    sys.exit(EXIT_CODE)

