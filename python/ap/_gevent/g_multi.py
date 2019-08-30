# -*- coding: utf-8 -*-
#
import gevent
import gevent.monkey
# import gevent.wsgi
import gevent.server
gevent.monkey.patch_all()

import logging
import logging.handlers
import multiprocessing


# 日志
def getLogger(name):
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
    _handler.setFormatter(logging.Formatter('%(asctime)s %(module)s %(levelname)s:%(lineno)s %(message)s'))
    log = logging.getLogger(name)
    log.addHandler(_handler)
    log.setLevel(logging.DEBUG)
    return log

log = getLogger(__name__)
signal_stop = False

################################################################################
def test():
    while 1:
        if signal_stop: break
        log.info("-------------------1----------------")
        gevent.sleep(1)

def test2():
    while 1:
        if signal_stop: break
        log.info("-------------------2----------------")
        gevent.sleep(2)

######################################################
# 信号量处理
def signal_handle(mode):
    log.info(u"catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

# --------------信号量处理---------------
# 设置监听信号量
# 设置程序结束信号量
def register_gevent_signal(handler):
    import signal
    import gevent.signal
    gevent.signal(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    gevent.signal(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    gevent.signal(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

def main():
    register_gevent_signal(signal_handle)
    gevent.joinall([
        gevent.spawn(test),
        gevent.spawn(test2),
    ])

if __name__ == '__main__':
    for i in range(3):
        process = multiprocessing.Process(target=main)
        process.start()