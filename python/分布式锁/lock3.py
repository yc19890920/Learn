# -*- coding:utf-8 -*-
import time
import redis
import logging

logger = logging.getLogger('service.redis_lock')
CONN = redis.Redis(host='192.168.1.24')

def acquire_lock(lockname, identifier, wait_time=20, timeout=15):
    end = time.time() + wait_time
    while end > time.time():
        if CONN.setnx(lockname, identifier):
            CONN.expire(lockname, timeout) # set expire time
            return identifier
        elif not redis.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
            redis.expire(lockname, timeout)
        time.sleep(0.001) # wait until the lock expired or release by some thread
    return False


def release_lock(lockname, identifier):
    pipe = CONN.pipeline(True)
    try:
        #watch lock once lock has been changed, break this transaction
        pipe.watch(lockname)
        #check if lock has been changed
        if pipe.get(lockname) == identifier:
            pipe.multi()
            pipe.delete(lockname)
            pipe.execute()
            return True

        pipe.unwatch() #execu when identifier not equal
    except redis.exceptions.WatchError as e:
        logger.error(e)
        return False
    except Exception as e:
        logger.error(e)
        return False

    return False


if __name__ == '__main__':
    print release_lock('h', 'a')