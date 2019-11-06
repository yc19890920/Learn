# -*- coding: utf-8 -*-
"""
签名 coockie
令牌 coockie
"""
import time

def checkToken(redis, token):
    return redis.hget("login:", token)

def updateToken(redis, token, user, item=None):
    """
    记录最后一次浏览商品的时间以及用户最近浏览了哪些商品。
    每秒至少可以记录20000件商品，比10台传统数据库6000次写入高3倍有余。
    """
    timestamp = time.time()
    p = redis.pipeline()
    # 维护令牌与已登录用户之间的映射
    p.hset("login:", token, user)
    # 记录令牌最好一次出现的时间
    p.zadd("login:recent:", {token: timestamp})
    if item:
        # 记录用户浏览过的商品
        p.zadd("viewed:"+token, {item: timestamp})
        # 移除旧的记录，只保留用户最近浏览过的25个商品
        p.zremrangebyrank("viewed:"+token, 0, -26)
    p.execute()


LIMIT = 10000000
LIMIT = 200
def cleanSessions(redis):
    """ 定时清理 session
    """
    while 1:
        size = redis.zcard("login:recent:")
        if size <= LIMIT:
            break
        # 获取需要移除的令牌
        end_index = min(size - LIMIT, 100)
        tokens = redis.zrange("login:recent:", 0, end_index-1)

        # 移除旧的令牌
        sessions_keys = ( "viewed:"+token for token in tokens)
        p = redis.pipeline()
        p.delete(*sessions_keys)
        p.hdel("login:", *tokens)
        p.zrem("login:recent:", *tokens)
        p.execute()



if __name__ == "__main__":
    import redis
    import random
    import uuid
    items = [i for i in range(1, 50)]
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)
    for j in range(200):
        for i in range(1, 2000):
            updateToken(redis, str(uuid.uuid1()), i, item=random.choice(items))
    cleanSessions(redis)