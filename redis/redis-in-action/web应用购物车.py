# -*- coding: utf-8 -*-
"""
购物车
网页缓存
数据行缓存
网页分析
"""

def add_to_cart(redis, session, item, count):
    """ 购物车添加
    """
    if count <= 0:
        redis.hrem("cart:"+session, item)
    else:
        redis.hset("cart:"+session, item, count)

LIMIT = 10000000
LIMIT = 200
def clean_full_seesions(redis):
    while 1:
        size = redis.zcard("login:recent:")
        if size <= LIMIT:
            break

        # 获取需要移除的令牌
        end_index = min(size - LIMIT, 100)
        tokens = redis.zrange("login:recent:", 0, end_index - 1)

        # 移除旧的令牌
        sessions_keys = ( "viewed:"+token for token in tokens)
        cart_sessions_keys = ("cart:" + token for token in tokens)
        p = redis.pipeline()
        p.delete(*sessions_keys)
        p.delete(*cart_sessions_keys)
        p.hdel("login:", *tokens)
        p.zrem("login:recent:", *tokens)
        p.execute()