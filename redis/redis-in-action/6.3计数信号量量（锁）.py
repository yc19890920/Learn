# -*- coding: utf-8 -*-
"""
计数信号量 是一种锁，它可以让用户限制一项资源最多能够同时被多少个进程访问，通常用于限定能够同时使用的资源数量。
计数信号量和其他锁的区别在于，当客户端获取锁失败的时候，客户端通常会选择进行等待；
而当客户端获取计数信号量失败的时候，客户端通常会选择立即返回失败结果。

基本的信号量：
    每当锁或者信号量因为系统时钟的细微不同而导致的获取结果出现剧烈变化时，这个锁或者信号量就是不公平的（unfair）.
    不公平的锁和信号量可能会导致客户端永远也无法获得它原本应该得到的锁或信号量。

公平信号量： 最先对计数器执行自增操作的客户端能够获得信号量。
为了满足“公平信号量”，程序会将计数器生成的值作为分值，存储到一个“信号量拥有者”有序集合里，然后通过检查客户端生成的标识符在有序集合中的排名来判断客户端是否取得了信号量。
另外，公平信号量实现还会通过ZINTERSTORE命令以及该命令的WEIGHTS参数，将信号量的超时时间传递给新的信号量拥有者有序集合。


最公平地信号量： 带锁的公平信号量。
"""
import time
import uuid
import redis

redis.zrem

def acquire_semaphore(redis, semname, limit, timeout=10):
    """
    每当锁或者信号量因为系统时钟的细微不同而导致的获取结果出现剧烈变化时，这个锁或者信号量就是不公平的（unfair）.
    不公平的锁和信号量可能会导致客户端永远也无法获得它原本应该得到的锁或信号量。
    :param redis:
    :param semname:
    :param limit:
    :param timeout:
    :return:
    """
    semname = "semaphore:" + semname
    ident = str(uuid.uuid4())
    now = time.time()

    p = redis.pipeline(True)
    # 清理过期的信号量持有者
    p.zremrangebyscore(semname, '-inf', now-timeout)
    # 尝试获取信号量
    p.zadd(semname, {ident: now})
    p.zrank(semname, ident)
    res = p.execute()
    if res[-1] < limit:
        return ident
    # 获取信号量失败，删除之前添加的标识符
    redis.zrem(semname, ident)
    return None

def release_semaphore(redis, semname, identifier):
    """
    :param redis:
    :param semname:
    :param identifier:
    :return:
    """
    # 如果信号量被正确删除则返回True; 返回False则表示该信号量已经因为过期而被删除了。
    semname = "semaphore:" + semname
    return redis.zrem(semname, identifier)


def acquire_fair_semaphore(redis, semname, limit, timeout=10):
    """ 首先通过从超时有序集合里面移除过期元素的方式来移除超时的信号量，
    接着对超时有序集合和信号量拥有者有序集合执行交集计算，
    并将计算结果保存到信号量拥有者有序集合里面，覆盖有序集合中原有的数据。
    之后，程序会对计数器执行自增操作，并将计数器生成的值添加到信号量拥有者有序集合里面；
    与此同时，程序还将当前的系统时间添加到超时有序集合里面。
    在完成以上操作之后，程序会检查当前客户端添加的标识符在信号量拥有者有序集合的排名是否足够低，如果是的话就表示客户端成功取得了信号量。
    相反地，如果客户端未能取得信号量，那么程序将从信号量拥有者有序集合以及超时有序集合里面移除与改客户端相关地元素。
    :param redis:
    :param semname:
    :param limit:
    :param timeout:
    :return:
    """
    semname = "semaphore:" + semname
    czset = "semaphore:owner:" + semname
    ctr = "semaphore:counter:" + semname
    ident = str(uuid.uuid4())
    now = time.time()
    p = redis.pipeline(True)
    # 删除超时地信号量
    p.zremrangebyscore(semname, '-inf', now-timeout)
    p.zinterstore(czset, {czset: 1, semname: 0})

    # 对计数器执行自增操作
    p.incr(ctr)
    counter = p.execute()[-1]

    # 尝试获取信号量。
    p.zadd(semname, {ident: now})
    p.zadd(czset, {ident: counter})

    # 通过检擦排名来判断客户端是否取得了信号量
    p.zrank(czset, ident)
    if p.execute()[-1] < limit:
        return ident

    p.zrem(semname, ident)
    p.zrem(czset, ident)
    p.execute()
    return None


def release_fair_semaphore(redis, semname, identifier):
    """
    :param redis:
    :param semname:
    :param identifier:
    :return:
    """
    # 如果信号量被正确删除则返回True; 返回False则表示该信号量已经因为过期而被删除了。
    semname = "semaphore:" + semname
    czset = "semaphore:owner:" + semname
    p = redis.pipeline(True)
    p.zrem(semname, identifier)
    p.zrem(czset, identifier)
    # 如果信号量被正确删除则返回True; 返回False则表示该信号量已经因为过期而被删除了。
    return p.execute()[0]

def refresh_fair_semaphore(redis, semname, identifier):
    semname = "semaphore:" + semname
    if redis.zadd(semname, {identifier: time.time()}):
        release_fair_semaphore(redis, semname, identifier)
        return False
    return True










