# coding: utf-8

import Queue
import threading
import time
import itertools
import random
import sys
import traceback
import signal

import logging
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(funcName)s:%(lineno)s %(message)s'))
log = logging.getLogger('Test')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

signal_stop=False


############################################################
# 信号量处理
def signal_handle(signum, frame):
    log.info("catch signal: %s"% signum)
    global signal_stop
    signal_stop = True

def init_signal(handler_exit):
    signal.signal(signal.SIGINT, handler_exit)  # 处理 Ctrl-C
    signal.signal(signal.SIGTERM, handler_exit)  # 处理 kill
    signal.signal(signal.SIGCHLD, handler_exit)  # 处理 signal.alarm()

init_signal(signal_handle)

############################################################
# 继承父类threading.Thread
class ConsumerThread(threading.Thread):
    '消费者'
    def __init__(self, threadID, queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.threadID = threadID

    # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
    def run(self):
        log.info("I am Consumer Thread-{}".format(self.threadID))
        while True:
            counter=self.queue.get()
            log.info('Going to Sleep Thread-{}: {}.'.format(self.threadID, counter))
            time.sleep(random.randint(1, 100) * 0.01)
            log.info('I am up        Thread-{}: {}.'.format(self.threadID, counter))
            self.queue.task_done()
            time.sleep(1)


############################################################
def producerLoop(queue):
    '生产者'
    _nxt = itertools.cycle(xrange(100))
    while 1:
        if signal_stop: break
        queue.put(_nxt.next())
        time.sleep(0.1)
    queue.join()

############################################################
def consumerThreadLoop(queue):
    _threads = []
    # 创建新线程
    for i in range(1, 11):
        _threads.append(ConsumerThread(i, queue))

    # 开启线程
    for worker in _threads:
        log.info('Going to start Thread!')
        worker.daemon=True
        worker.start()

############################################################
def main():
    # Python 中的Queue实现了经典的先入先出队列，并且是线程安全的。
    # 队列长度可为无限或者有限。可通过Queue的构造函数的可选参数maxsize来设定队列长度。如果maxsize小于1就表示队列长度无限。
    queue = Queue.Queue(50)
    consumerThreadLoop(queue)
    producerLoop(queue)
    return

if __name__ == "__main__":
    log.info( u'program start...' )
    EXIT_CODE=0
    try:
        main()
    except:
        print traceback.format_exc()
        EXIT_CODE = 1
    log.info( "program quit..." )
    sys.exit(EXIT_CODE)

