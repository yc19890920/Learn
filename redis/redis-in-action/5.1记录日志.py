# -*- coding: utf-8 -*-

import time
import logging
import datetime
import redis
from redis.exceptions import WatchError

SERVERITY = {
    logging.DEBUG: 'debug',
    logging.INFO: 'info',
    logging.WARNING: 'warning',
    logging.ERROR: 'error',
    logging.CRITICAL: 'critical',
}

SERVERITY.update((name, name) for name in SERVERITY.values())


def log_recent(redis, name, message, severity=logging.INFO, pipe=None):
    """ 最新日志查询
    :param redis:
    :param name: 创建负责存储的消息键
    :param message:  消息
    :param severity:  级别
    :param pipe:
    :return:
    """
    severity = str( SERVERITY.get(severity, severity) ).lower()
    destination = 'log:recent:%s:%s' % (name, severity)
    message = time.asctime() + ' ' + message
    p = pipe or redis.pipeline()
    p.lpush(destination, message)
    # 对日志进行修剪，只保存最新的100条记录
    p.ltrim(destination, 0, 99)
    p.execute()


def log_common(redis, name, message, severity=logging.INFO, pipe=None, timeout=5):
    """ 常见日志
    程序将消息作为成员存储到有序集合里面，并将消息出现的频率对消息进行轮换，
    并在轮换日志的时候保留上一个小时记录的常见消息，从而防止没有任何消息存在的情况出现。
    :param redis:
    :param name:
    :param message:
    :param severity:
    :param pipe:
    :param timeout:
    :return:
    """
    severity = str(SERVERITY.get(severity, severity)).lower()
    destination = 'log:common:%s:%s' % (name, severity)
    start_key = destination + ':start'
    end = time.time() + timeout
    p = pipe or redis.pipeline()
    while time.time() < end:
        try:
            # 对记录当前小时数的键进行监控，确保轮换操作可以正确的执行。
            p.watch(start_key)
            now = datetime.datetime.utcnow().timetuple()
            # 取得当前所处的小时数
            hour_start = datetime.datetime(*now[:4]).isoformat()
            existing = p.get(start_key)
            p.setnx(start_key, hour_start)
            p.multi()
            # 如果这个常见日志消息列表记录的是上一个小时的日志...
            if existing and existing < hour_start:
                p.rename(destination, destination + ":last")
                p.rename(start_key, destination + ':pstart')
                p.set(start_key, hour_start)
            p.zincrby(destination, 1, message)
            log_recent(redis, name, message, severity, p)
            return
        except WatchError as e:
            pass


if __name__ == "__main__":
    import random
    t = time.time()
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)
    names = [
        "AAA", "BBB", "CCC"
    ]
    messages = [
        "message %d" % i for i in range(1, 100)
    ]
    for i in range(100000):
        name = random.choice(names)
        message = random.choice(messages)
        log_common(redis, name, message, severity=logging.INFO, pipe=None, timeout=5)
    print time.time() - t

