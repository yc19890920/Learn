# -*- coding: utf-8 -*-
from threading import RLock
from functools import wraps

class LruCache(object):
    '''不能存储可变类型对象，不能并发访问set()'''

    def __init__(self, capacity):
        self.l = []
        self.d = {}
        self.capacity = capacity

    def get(self, key):
        if self.d.has_key(key):
            value = self.d[key]
            self.l.remove(key)
            self.l.insert(0, key)
        else:
            value = None

        return value

    def add(self, key, value):
        if self.d.has_key(key):
            self.l.remove(key)
        elif len(self.d) == self.capacity:
            oldest_key = self.l.pop()
            self.d.pop(oldest_key)

        self.d[key] = value
        self.l.insert(0, key)


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

    t = time.time()
    for i in range(1, 101):
        print fab(i)
    print time.time() - t
    # 354224848179261915075
    # 0.0090000629425
