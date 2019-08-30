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
lock = asyncio.Lock()
redis = StrictRedis(host='127.0.0.1', port=6379, db=0)

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

class MyPoolDB:

    async def init_pool(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
            # print('-------1---------', loop)
        pool = await aiomysql.create_pool(
            loop=loop,
            host='127.0.0.1',
            port=3306,
            user='bankbin',
            password='ysqzx6388260',
            db='bankbin',
            charset='utf8',
            autocommit=True,
            maxsize=10,
            minsize=1
        )
        return pool

    async def Query(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            r = await cur.fetchall()
        pool.close()
        await pool.wait_closed()
        return r

    async def QueryOne(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            r = await cur.fetchone()
        pool.close()
        await pool.wait_closed()
        return r

    async def QueryWithDictCursor(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor(DictCursor)
            await cur.execute(sql, args)
            r = await cur.fetchall()
        pool.close()
        await pool.wait_closed()
        return r

    async def QueryOneWithDictCursor(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor(DictCursor)
            await cur.execute(sql, args)
            r = await cur.fetchone()
        pool.close()
        await pool.wait_closed()
        return r

    async def DBQueryExt(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            r = await cur.fetchall()
            names = [i[0] for i in cur.description]
        pool.close()
        await pool.wait_closed()
        return names, r

    async def Do(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            await conn.commit()
        pool.close()
        await pool.wait_closed()
        return True

    async def DoMany(self, sql, args=[], loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor()
            await cur.executemany(sql, args)
            await conn.commit()
        pool.close()
        await pool.wait_closed()
        return True

    async def DoReturnID(self, sql, args=(), loop=None):
        pool = await self.init_pool(loop)
        with await pool as conn:
            cur = await conn.cursor()
            await cur.execute(sql, args)
            await conn.commit()
            lastrowid = cur.lastrowid
        pool.close()
        await pool.wait_closed()
        return lastrowid

My = MyPoolDB()


async def rA():
    while 1:
        if signal_stop: break
        sql = "SELECT * FROM `auth_user` WHERE 1 limit 1"
        _ = await My.Query(sql)
        log.info("ra:{}".format(_))
        await asyncio.sleep(2)

async def rB():
    while 1:
        if signal_stop: break
        # sql = "SELECT * FROM `auth_user` WHERE 1 limit 1"
        # _ = await My.QueryOneWithDictCursor(sql)
        # _ = await My.DBQueryExt(sql)
        sql = "INSERT INTO auth_group(name) VALUES (%s) ON DUPLICATE KEY IGNORE;"
        sql = "INSERT IGNORE INTO auth_group(name) VALUES (%s);"
        # sql = "INSERT INTO auth_group(name) VALUES (%s) ON conflict (name) do UPDATE SET"
        # sql = "INSERT INTO `auth_group`(`name`) VALUES ('abc');"
        _ = await My.DoReturnID(sql, ('dbd',))
        log.info("---------rb:{}".format(_))
        await asyncio.sleep(5)


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

    # 执行coroutine
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end = time.time()
    log.info("Total Time: {}".format(end - start))

if __name__ == "__main__":
    log.info("program start...")
    main()
    log.info("program end...")



