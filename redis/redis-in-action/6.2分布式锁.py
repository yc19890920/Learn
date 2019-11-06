# -*- coding: utf-8 -*-
"""
1. 构建两个前缀匹配自动补全程序
2. 构建分布式锁提高性能
3. 通过开发计数信号量来控制并发
4. 构建两个不同用途的任务队列
5. 通过消息拉取系统来实现延迟消息传递
6. 学习如何进行文件分发


对数据进行加锁时，首先获取锁来得到对数据进行排他性访问，然后才能对数据进行一系列操作，最后再释放锁。

共享内存数据结构： 获取锁，执行操作，释放锁。

redis watch命令来代替对数据进行加锁，因为watch只会在数据b被其他客户端抢先修改了的情况下通知执行了这个命令的客户端，而不会阻止其他客户端对数据进行修改，
所以这个命令被称为乐观锁（optimistic locking）

分布式锁也有类似的“获取锁，执行操作，释放锁”动作，但这种锁既不是给同一个进程种的多个线程使用，也不是给同一台机器上的多个进程使用，
而是由不同机器上的不同redis客户端进行获取和释放的。

有的应用不需要锁可以正确运行；
有的使用少量的锁；
还有的应用需要每个步骤都使用锁。

操作系统级别的锁，编程语言级别的锁，其他锁，
redis 构建锁

setex具备加锁功能，但功能并不完整，也不具备分布式锁常见的一些高级特性。

使用watch命令来监视b被频繁访问的键可能会引起性能问题，
构建锁的详细步骤，并最终某些情况下使用锁去代替watch命令。

watch,multi, exec 组成的事务并不具有可扩展性，原因在于程序在尝试完成一个事务的时候，可能会因为事务执行失败而反复的重试。

导致锁出现不正确行为的原因，以及锁在不正确运行时的症状：
1. 持有锁的进程因为操作时间过长而导致锁被自动释放，但进程本身并不知晓这一点，甚至还可能会错误地释放掉了其他进程持有地锁。
2. 一个持有锁打算执行长时间操作地进程已经崩溃，但其他想要获取锁地进程不知道哪个进程持有着锁，也无法检测出持有锁的进程已经崩溃，只能白白的浪费时间等待锁被释放。
3.在一个进程持有的锁过期后，其他多个进程同时尝试去获取锁，并且都获得了锁。
4. 上面第一种和第三种情况同时出现，导致多个进程获得了锁，而每个进程都以为自己是唯一一个获得锁的进程。


正确地实现基本地加锁，如何处理过期地锁，以及因为持有者崩溃而无法释放地锁。

细粒度锁，只锁住要被购买的商品而不是整个市场，可以减少锁竞争出现的几率并提升程序的性能。
"""
import time
import uuid
import redis
import math
from redis.exceptions import WatchError

def acquire_lock(redis, lockname, acquire_timeout=10):
    """
    正确地实现基本地加锁， (没有超时时间的锁)
    setnx 命令天生就适用来实现锁地获取功能，这个命令只会在键不存在地情况下为键设置值，
    而锁要做的就是将一个随机生成的128位uuid设置为键的值，并使用这个值来防止锁被其他进程取得。
    :param redis:
    :param lockname:   锁名称
    :param acquire_timeout:
    :return:
    """
    ident = str(uuid.uuid4())
    end = time.time() + acquire_timeout
    lockname = "lock:"+lockname
    while time.time() < end:
        if redis.setnx(lockname, ident):
            return ident
        # elif not redis.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
        #     redis.expire(lockname, lock_timeout)
        time.sleep(0.001)
    return None

def acquire_lock_with_timeout(redis, lockname, acquire_timeout=10, lock_timeout=30):
    """
    正确地实现基本地加锁， (设置超时时间的锁)
    setnx 命令天生就适用来实现锁地获取功能，这个命令只会在键不存在地情况下为键设置值，
    而锁要做的就是将一个随机生成的128位uuid设置为键的值，并使用这个值来防止锁被其他进程取得。
    :param redis:
    :param lockname:   锁名称
    :param acquire_timeout:
    :return:
    """
    identifire = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    end = time.time() + acquire_timeout
    # 确保传给EXPIRE的都是整数
    lock_timeout = int(math.ceil(lock_timeout))
    while time.time() < end:
        if redis.setnx(lockname, identifire):  # 以锁名称为键，uuid的值为值，redis服务器setnx保证了只能有一个客户端成功设置键的原子性
            redis.expire(lockname, lock_timeout)  # 设置键的过期时间，过期自动剔除，释放锁
            return identifire
        elif not redis.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
            redis.expire(lockname, lock_timeout)
        time.sleep(0.001)
    return None

def acquire_lock_with_timeout2(redis, lockname, acquire_timeout=10, lock_timeout=30):
    """
    正确地实现基本地加锁， (设置超时时间的锁)
    setnx 命令天生就适用来实现锁地获取功能，这个命令只会在键不存在地情况下为键设置值，
    而锁要做的就是将一个随机生成的128位uuid设置为键的值，并使用这个值来防止锁被其他进程取得。

     set(name, value, ex=None, px=None, nx=False, xx=False)
     ex，过期时间（秒）
     px，过期时间（毫秒）
     nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
     xx，如果设置为True，则只有name存在时，当前set操作才执行'''

    setex(name, value, time)
    #设置过期时间（秒）

    psetex(name, time_ms, value)
    #设置过期时间（豪秒）

    :param redis:
    :param lockname:   锁名称
    :param acquire_timeout:
    :return:
    """
    identifire = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    end = time.time() + acquire_timeout
    # 确保传给EXPIRE的都是整数
    lock_timeout = int(math.ceil(lock_timeout))
    while time.time() < end:
        if redis.set(lockname, identifire, ex=lock_timeout, nx=True):  # 以锁名称为键，uuid的值为值，redis服务器setnx保证了只能有一个客户端成功设置键的原子性
            # redis.expire(lockname, lock_timeout)  # 设置键的过期时间，过期自动剔除，释放锁
            return identifire
        elif not redis.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
            redis.expire(lockname, lock_timeout)
        time.sleep(0.001)
    return None


def release_lock(redis, lockname, identifier):
    """ 释放锁
    :param redis:
    :param lockname:
    :param identifier:
    :return:
    """
    p = redis.pipeline(True)
    lockname = "lock:"+lockname
    while 1:
        try:
            p.watch(lockname)
            if p.get(lockname) == identifier:
                p.multi()
                p.delete(lockname)
                p.execute()
                return True
            p.unwatch()
            break
        except WatchError:
            pass
    return False

################################################################################################################################################
# 细粒度锁，只锁住要被购买的商品而不是整个市场，可以减少锁竞争出现的几率并提升程序的性能。


################################################################################################################################################
def listItem(redis, itemid, sellerid, price):
    """ 售卖商品
    将商品放到市场上销售，程序需要将被销售的商品添加到记录市场正在销售商品的有序集合里面，
    并且在添加操作执行的过程中，监视卖家的包裹以确保被销售的商品的确存在于卖家的包裹中。
    :param redis:
    :param itemid:
    :param sellerid:
    :param price:
    :return:
    """
    inventory = "test:inventory:%s" % str(sellerid)
    item = "%s.%s" % (str(itemid), str(sellerid))
    end = time.time()+5
    p = redis.pipeline()
    while time.time() < end:
        try:
            # 监视用户包裹发生的变化
            p.watch(inventory)
            # 如果指定的商品不在用户的包裹里面，那么停止对包裹的监视并返回一个空值
            if not p.sismember(inventory, itemid):
                p.unwatch()
                return 3

            # 把销售的商品添加到商品买卖市场里面。
            p.multi()
            p.zadd("test:market:", {
                item: price
            })
            p.srem(inventory, itemid)
            # 如果执行execute方法没有引发WatchError异常，那么说明事务执行成功，并且对包裹键的监视也已经结束。
            p.execute()
            return 1
        except WatchError: # 用户的包裹已经发生了变化，重试。
            pass
    return 2

def purchase_item(redis, buyerid, itemid, sellerid, lprice):
    buyer = "test:users:%s" % str(buyerid)
    seller = "test:users:%s" % str(sellerid)
    item = "%s.%s" % (str(itemid), str(sellerid))
    inventory = "test:inventory:%s" % str(buyerid)

    # 尝试获取锁
    market = "test:market:"
    ident = acquire_lock(redis, market, acquire_timeout=10)
    if not ident:
        return 2

    p = redis.pipeline(True)
    try:
        p.zscore(market, item)
        p.hget(buyer, "funds")
        price, funds = p.execute()
        # 钱不够
        if price is None or funds < 0 or price != lprice or price > funds:
            return 3
        p.hincrby(seller, "funds", int(price))
        p.hincrby(buyer, "funds", -int(price))
        p.sadd(inventory, itemid)
        p.zrem("test:market:", item)
        p.execute()
        return 1
    except:
        return 4
    finally:
        release_lock(redis, market, ident)


    # end = time.time()+5
    # p = redis.pipeline()
    # while time.time() < end:
    #     try:
    #         # 对商品买卖市场以及买家的个人信息进行监视。
    #         # 监视商品是确保m买家想要购买的商品仍然有售（或者商品被别人）
    #         p.watch("test:market:", buyer)
    #
    #         price = p.zscore("test:market:", item)
    #         funds = int(p.hget(buyer, "funds"))
    #         # 钱不够
    #         if funds <0 or price != lprice or price>funds:
    #             p.unwatch()
    #             return 3
    #
    #         # 将买家支付的钱转移给卖家，然后将被购买的商品转交给买家
    #         p.multi()
    #         p.hincrby(seller, "funds", int(price))
    #         p.hincrby(buyer, "funds", -int(price))
    #         p.sadd(inventory, itemid)
    #         p.zrem("test:market:", item)
    #         p.execute()
    #         return 1
    #     except WatchError:
    #         pass
    # return 2

if __name__ == "__main__":
    import random
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)
    users = [
        # {"id": i, "name": u"yc{}".format(i), "funds": random.uniform(50, 100)} for i in range(1, 1000)
        {"id": i, "name": u"yc{}".format(i), "funds": random.randint(20, 100)} for i in range(1, 5)
    ]
    p = redis.pipeline()
    for i in range(1, 5):
        p.hmset("test:users:%d" % i, {"id": i, "name": u"yc{}".format(i), "funds": random.randint(10, 100)})
    p.execute()

    for i in range(1, 5):
        print "user%d: "% i, redis.hgetall("test:users:%d" % i)

    items1 = (
        {"id": 1, "name": "ItemA", "price": random.randint(50, 100)},
        {"id": 2, "name": "ItemB", "price": random.randint(50, 100)},
        {"id": 3, "name": "ItemB", "price": random.randint(50, 100)},
        {"id": 4, "name": "ItemC", "price": random.randint(50, 100)},
        {"id": 5, "name": "ItemD", "price": random.randint(50, 100)},
        {"id": 6, "name": "ItemE", "price": random.randint(50, 100)},
    )
    p = redis.pipeline()
    for i in range(1, 5):
        for j in items1:
            inventory = "test:inventory:%s" % str(i)
            p.sadd(inventory, j["id"])
            # item = "%s.%s" % (str(j["id"]), str(i))
            # p.zadd("test:market:", {
            #     item: j["price"]
            # })
    p.execute()

    itemid = 1
    sellerid = 1
    price = items1[0]['price']
    res = listItem(redis, itemid, sellerid, price)
    print res

    # purchase_item(redis, buyerid, itemid, sellerid, lprice)
    buyerid = 2
    sellerid = 1
    lprice = items1[0]['price']
    res = purchase_item(redis, buyerid, itemid, sellerid, lprice)
    print res

    time.sleep(3600)
    lst = redis.keys("test:*")
    redis.delete(*lst)
































