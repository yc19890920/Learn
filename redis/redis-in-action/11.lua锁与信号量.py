# -*- coding: utf-8 -*-
"""
lua版本的锁性能较高。
"""

import uuid
import redis
import math
import time
from redis.exceptions import WatchError

################################################################################################################################################
# lua锁
def acquire_lock_with_timeout(redis, lockname, acquire_timeout=10, lock_timeout=60):
    """
    :param redis:
    :param lockname:
    :param acquire_timeout:
    :param lock_timeout:
    :return:
    """
    identifier = str(uuid.uuid4())
    lockname = "lock:"+ lockname
    lock_timeout = int(math.ceil(lock_timeout))
    acquired = False
    end = time.time() + acquire_timeout
    while time.time() < end and not acquired:
        acquired = acquire_lock_with_timeout_lua(redis, lockname, lock_timeout, identifier) == "OK"
        time.sleep(0.001*(not acquired))
    return acquired and identifier or None

def acquire_lock_with_timeout_lua(redis, lockname, lock_timeout, identifier):
    lua = redis.register_script("""
    if redis.call('exists', KEYS[1]) == 0 then
        return redis.call('setex', KEYS[1], unpack(ARGV))
    end
    """)
    return lua(keys=[lockname], args=[lock_timeout, identifier])

def release_lock(redis, lockname, identifier):
    lockname = "lock:" + lockname
    return release_lock_lua(redis, lockname, identifier)

def release_lock_lua(redis, lockname, identifier):
    lua = redis.register_script("""
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1]) or true
    end
    """)
    return lua(keys=[lockname], args=[identifier])


################################################################################################################################################
# lua信号量
def acquire_semaphore(redis, semname, limit, timeout=10):
    semname = "semaphore:" + semname
    ident = str(uuid.uuid4())
    now = time.time()

    # 清除所有已过期信号量
    # 如果还有剩余的信号量可用，那么获取信号量
    lua = redis.register_script("""
    redis.call('ZREMRANGEBYSCORE', KEYS[1], '-inf', ARGV[1])

    if redis.call('ZCARD', KEYS[1]) < tonumber(ARGV[2]) then
        redis.call('zadd', KEYS[1], ARGV[3], ARGV[4])
        return ARGV[4]
    end
    """)

    return lua(keys=[semname], args=[now-timeout, limit, now, ident])

def release_semaphore(redis, semname, identifier):
    # 如果信号量被正确删除则返回True; 返回False则表示该信号量已经因为过期而被删除了。
    semname = "semaphore:" + semname
    return redis.zrem(semname, identifier)

if __name__ == "__main__":
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)
    t = time.clock()
    index = 1
    end = time.time() + 10
    while time.time()<end:
        # identifier = acquire_lock_with_timeout(redis, str(index), acquire_timeout=10, lock_timeout=60)
        # print ident
        # release_lock(redis, str(index), identifier)
        # index += 1

        identifier = acquire_semaphore(redis, "aa", 5, timeout=10)
        print identifier
        time.sleep(0.2)
        if identifier:
            release_semaphore(redis, "aa", identifier)
            pass

    print index
    print time.clock() - t