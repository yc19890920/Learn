# -*- encoding: utf-8 -*-
import time
from functools import wraps, update_wrapper

def timeit(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        T = time.time()
        ret = func(*args, **kwargs)
        return ret, time.time()-T
    return wrapped

def memoize(fn):
    cache = dict()

    @wraps(fn)
    def memoizer(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return memoizer

def memoize2(fn):
    cache = dict()

    # @wraps(fn)
    def memoizer(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return update_wrapper(memoizer, fn)


@memoize
def fibonacci(n):
    assert(n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fibonacci(n-1) + fibonacci(n-2)

@memoize2
def fibonacci2(n):
    assert(n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fibonacci(n-1) + fibonacci(n-2)

if __name__ == '__main__':
    # print fibonacci(200)
    print fibonacci2(201)