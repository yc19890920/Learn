# -*- coding:utf-8 -*-
"""
https://github.com/NoneGG/aredis

"""
import time
import logging
import asyncio
import uvloop
import aiomysql
from aiomysql.cursors import DictCursor
from aredis import StrictRedis
from datetime import datetime
from motor import motor_asyncio
lock = asyncio.Lock()
redis = StrictRedis(host='127.0.0.1', port=6379, db=0)
from motor.motor_asyncio import AsyncIOMotorClient

def get_mongo_connection(loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    client = AsyncIOMotorClient("mongodb://mm-mc:PFBgatL4Vq63sEP@127.0.0.1:27017", io_loop=loop)
    return client['mm-mc']

# mongo_connection = AsyncIOMotorClient("mongodb://mm-mc:PFBgatL4Vq63sEP@127.0.0.1:27017")
# mongo = mongo_connection['mm-mc']

# contacts = mongo_connection.mydatabase.contacts
# mongo = motor_asyncio.AsyncIOMotorClient('mongodb://mm-mc:PFBgatL4Vq63sEP@127.0.0.1:27017/mm-mc')

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


async def rA():
    while 1:
        if signal_stop: break
        _ = await mongo.invalidqq.find_one({'addr': "18932418429@qq.com"})
        log.info("ra:{}".format(_))
        await asyncio.sleep(2)

async def rB():
    while 1:
        if signal_stop: break
        # cursor = mongo.invalidqq.find({'addr': "2@qq.com"})
        data = await mongo.invalidqq.find({'addr': "2@qq.com"}).to_list(20)
        for document in data:
            log.info("rb:{}".format(document))
        await asyncio.sleep(2)


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
    global mongo
    start = time.time()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 监听信号
    register_asyncio_signal(loop, signal_handler)
    # print('-------2---------', loop)
    tasks = [
        asyncio.ensure_future(rA()),
        asyncio.ensure_future(rB()),
    ]
    mongo = get_mongo_connection(loop)

    # 执行coroutine
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end = time.time()
    log.info("Total Time: {}".format(end - start))

if __name__ == "__main__":
    log.info("program start...")
    main()
    log.info("program end...")



