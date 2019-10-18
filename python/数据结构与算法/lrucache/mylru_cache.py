# -*- coding: utf-8 -*-
from collections import OrderedDict
from functools import wraps
from threading import RLock

class LruCache(OrderedDict):

    def __init__(self, maxsize=128, *args, **kwds):
        self.maxsize = maxsize
        if not isinstance(maxsize, int) or not self.maxsize:
            raise TypeError('Expected maxsize to be an integer and must gt 0')
        super(LruCache, self).__init__(*args, **kwds)

    def add(self, key, value):
        # 当缓存满了，需要添加新东西就移除最早的
        # 删除最早的条目
        if key not in self and self.maxsize <= len(self):
            self.popitem(last=False)
        self[key] = value

class _HashedSeq(list):
    """ This class guarantees that hash() will be called no more than once
        per element.  This is important because the lru_cache() will hash
        the key multiple times on a cache miss.

    """

    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue

def _make_key(args, kwds, typed=False,
              kwd_mark = (object(),),
              fasttypes = {int, str},
              tuple=tuple, type=type, len=len):
    """Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

    """
    # All of code below relies on kwds preserving the order input by the user.
    # Formerly, we sorted() the kwds before looping.  The new way is *much*
    # faster; however, it means that f(x=1, y=2) will now be treated as a
    # distinct call from f(y=2, x=1) which will be cached separately.
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item
        # print key
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for v in kwds.values())
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)

import hashlib
import json
def _make_key2(args, kwargs, typed=False):
    return hashlib.md5(
        json.dumps({
            'args': args,
            'kwargs': kwargs,
        }, sort_keys=True).encode('utf-8')
    ).hexdigest()

def lru_cache(typed=False, maxsize=128, make_key=_make_key):
    def lru_cache_wrapper(func):
        cache = LruCache(maxsize)
        lock = RLock()
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                key = make_key(args, kwargs, typed=False)
                value = cache.get(key)
                if value is None:
                    value = func(*args, **kwargs)
                    cache.add(key, value)
                return value
        return wrapper
    return lru_cache_wrapper

@lru_cache(typed=False, maxsize=128, make_key=_make_key)
def fab(n):
    if n <=2:
        return 1
    return fab(n-1) + fab(n-2)


if __name__ == "__main__":
    import time
    keys = ['test', 'red', 'fox', 'fence', 'junk', 'other', "test"]
    cache = LruCache(maxsize=3)
    for i, key in enumerate(keys):
        # if key in cache:
        #     continue
        # else:
        value = key
        # time.sleep(1)
        cache.add(key, value)
        print cache

    for i in cache.items():
        print(i)

    t = time.time()
    for i in range(1, 101):
        print fab(i)

    # _make_key  可能报错
    # 354224848179261915075
    # 0.000999927520752

    # _make_key2  不会报错
    # 354224848179261915075
    # 0.0130000114441
    print time.time() - t