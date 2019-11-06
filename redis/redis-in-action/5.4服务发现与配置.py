# -*- coding: utf-8 -*-
"""
随着我们越来越多地使用Redis以及其他服务，如何存储各项服务的配置信息将变成一个棘手的问题：
针对多个从服务器的Redis主服务器，数据库主从服务器。

用于连接其他服务以及服务器的配置信息一般都是以配置文件的形式存储在硬盘里面，
每当机器下线，网络连接断开或者某些需要连接其他服务器的情况时，程序通常需要一次性地对不同服务器中地多个配置文件进行更新。

如何将大部分配置信息从文件转移到redis里面，使得应用程序可以自己完成绝大部分配置工作。
"""
import time
import json
from functools import wraps
import redis

LAST_CHECKED = None
IS_UNDER_MAINTENANCE = False

EMPTY = object()

def is_under_maintenance(redis):
    # 将两个变量设置为全局变量以便在之后对它们进行写入
    global LAST_CHECKED, IS_UNDER_MAINTENANCE
    if not LAST_CHECKED:
        LAST_CHECKED = time.time()

    if LAST_CHECKED < time.time() - 1:
        LAST_CHECKED = time.time()
        IS_UNDER_MAINTENANCE = bool(redis.get('is-under-maintenance'))

    return IS_UNDER_MAINTENANCE

def set_config(redis, typ, component, config):
    """
    :param redis:
    :param typ:
    :param component:
    :param config:
    :return:
    """
    redis.set(
        'config:%s:%s' % (typ, component),
        json.dumps(config)
    )

CONGIGS = {}
CHECKED = {}

def get_config(redis, typ, component, wait=1):
    key = 'config:%s:%s' % (typ, component)

    if CHECKED.get(key, time.time()) < time.time() - wait:
        CHECKED[key] = time.time()
        config = json.loads(redis.get(key) or '{}')
        old_config = CONGIGS.get(key)
        if config != old_config:
            CONGIGS[key] = config
        return CONGIGS.get(key)


REDIS_CONNECTIONS = {}

def redis_connection(component, wait=1):
    key = "config:redis:" + component
    def wrapper(func):
        @wraps(func)
        def caller(*args, **kwargs):
            old_config = CONGIGS.get(key, EMPTY)
            config = get_config(config_connection, "redis", component, wait=wait)
            # config = {}
            if config != old_config:
                REDIS_CONNECTIONS[key] = redis.Redis(**config)
            return func(REDIS_CONNECTIONS.get(key), *args, **kwargs)
        return caller
    return wrapper























