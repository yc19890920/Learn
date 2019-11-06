# -*- coding: utf-8 -*-

import time
import logging
import datetime
import redis
import bisect
from redis.exceptions import WatchError

# 以秒为单位的计数器精度，分别为1秒，5秒，1分钟，5分钟，1小时，5小时，1天——用户可以按需调整这些精度。
PRECISION = [1, 5, 60, 300, 3600, 18000, 86400]

def update_counter(redis, name, count=1, now=None):
    """
    :param redis:
    :param name:
    :param count:
    :param now:
    :return:
    """
    # 取得当前时间来判断应该对哪个时间执行自增操作
    now = now or time.time()
    p = redis.pipeline()
    for prec in PRECISION:
        # 取得当前时间片的开始时间
        pnow = int(now/prec) * prec
        # 创建负责存储计数信息的散列。
        hash = '%s:%s' % (prec, name)
        # 将计数器的引用信息添加到有序集合里面，并将其分值设为0， 以便在之后执行清理操作。 都为0，则会根据成员名进行排序了。
        p.zadd('test:known:', {hash: 0})
        # 对给定m名字和精度的计数器进行更新
        p.hincrby('test:count:' + hash, pnow, count)
    p.execute()

def get_counter(redis, name, precision):
    """
    :param redis:
    :param name:
    :param precision:
    :return:
    """
    hash = '%s:%s' % (precision, name)
    data = redis.hgetall('test:count:' + hash)
    ret = [(int(key), int(value)) for key, value in data.iteritems()]
    ret.sort()
    return ret

SAMPLE_COUNT = 120
def clean_counter(redis):
    """ 清理计数器，保留最新的120个样本
    :param redis:
    :return:
    """
    # 为了平等地处理更新频率各不相同的多个计数器，程序需要记录清理操作执行的次数。
    passes = 0
    while 1:
        p = redis.pipeline(True)
        start = time.time()
        # 渐进地遍历所有已知的计数器
        index = 0
        while index<redis.zcard('test:known:'):
            # 取得被检擦计数器的数据
            hash = redis.zrange('test:known:', index, index)
            index += 1
            if not hash:
                break
            hash = hash[0]
            prec = int(hash.partition(":")[0])
            # 因为清理程序每60秒就会循环一次，所以需要根据计数器的更新频率来判断是否真的有必要对计数器进行清理。
            bprec = int(prec//60) or 1
            # 如果整个计数器在这次循环里不需要进行清理，那么检擦下一个计数器
            if passes % bprec:
                continue
            hkey = 'test:count:' + hash
            # print hkey
            # 更具给定的精度以及需要b保留的样本数量，计算出我们需要保留什么时间之前的样本。
            cutoff = time.time() - SAMPLE_COUNT * prec
            samples = map(int, redis.hkeys(hkey))
            samples.sort()
            remove = bisect.bisect_right(samples, cutoff)
            if remove:
                print "==========================================="
                print hkey, samples[:remove]
                redis.hdel(hkey, *samples[:remove])
                if remove == len(samples):
                    try:
                        # 尝试修改计数器散列之前对其进行监视
                        p.watch(hkey)
                        if not p.hlen(hkey):
                            p.multi()
                            p.zrem('test:known:', hash)
                            p.execute()
                            # 在删除一个计数器的情况下，下次循环可以使用与本次循环相同的索引
                            index -= 1
                        else:
                            p.unwatch()
                    except WatchError:
                        pass
        passes += 1
        duration = min(int(time.time()-start)+1, 60)
        print "sleep"
        time.sleep(max(60-duration, 1))


if __name__ == "__main__":
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)

    index = 1
    while 1:
        update_counter(redis, 'hits', count=1)
        time.sleep(0.1)
        index += 1
        if index%100==0:
            print get_counter(redis, "hits", 5)
        if index>18000:
            break

    clean_counter(redis)




