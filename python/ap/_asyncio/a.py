# -*- coding:utf-8 -*-
import time
import logging
import asyncio
import uvloop
from datetime import datetime
lock = asyncio.Lock()

def getLogger(name):
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
    _handler.setFormatter(logging.Formatter('%(asctime)s %(module)s %(levelname)s:%(lineno)s %(message)s'))
    log = logging.getLogger(name)
    log.addHandler(_handler)
    log.setLevel(logging.DEBUG)
    return log

log = getLogger(__name__)
signal_stop=False

async def custom_sleep(name, uuid, sleep):
    await asyncio.sleep(sleep)
    print('Task {}, uuid: {}, time:{})'.format(name, uuid, datetime.now()))

async def factorial(name, number):
    global uuid
    f = i = 1
    while 1:
        if signal_stop: break
        with await lock:  uuid += 1
        print('Task {}, uuid: {}, Compute factorial({})'.format(name, uuid, i))
        await custom_sleep(name, uuid, number)
        f *= i
        i += 1

######################################################
# --------------信号量处理---------------
# 信号量处理
def signal_handler(mode):
    log.info(u"catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

# 设置监听信号量
def register_asyncio_signal(loop, handler):
    import signal
    loop.add_signal_handler(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    loop.add_signal_handler(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    loop.add_signal_handler(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

######################################################
def main():
    global uuid
    uuid = 0
    start = time.time()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 监听信号
    register_asyncio_signal(loop, signal_handler)

    tasks = [asyncio.ensure_future(factorial("A", 1)) for i in range(1)]
    tasks.extend([asyncio.ensure_future(factorial("B", 2)) for i in range(2)])
    # tasks = [
    #     asyncio.ensure_future(factorial("A", 1)),
    #     asyncio.ensure_future(factorial("B", 2)),
    # ]

    # 执行coroutine
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end = time.time()
    log.info("Total Time: {}".format(end - start))

if __name__ == "__main__":
    log.info("program start...")
    main()
    log.info("program end...")



