#-*-coding:utf8-*-
import datetime
now = datetime.datetime.now
from functools import wraps

def cache(func):

    caches = {}
    @wraps(func)
    def wrap(*args):
        if args not in caches:
            caches[args] = func(*args)
        return caches[args]
    return wrap

@cache
def fib(num):
    if num < 2:
        return 1
    return fib(num-1) + fib(num-2)


for i in range(10):
    print fib(i)


# ----------------------------

from collections import OrderedDict

## 保留 最近的5个数据缓存
class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self.__capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self.__capacity:
            last = self.popitem(last=False)
            # print 'remove:', last
        if containsKey:
            del self[key]
        #     print 'set:', (key, value)
        # else:
        #     print 'add:', (key, value)
        OrderedDict.__setitem__(self, key, value)

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapped(args, **kwargs):
            if args not in self:
                self[args] = func(args)
            print self
            return self[args]
        return wrapped

@LastUpdatedOrderedDict(capacity=5)
def fib2(num):
    if num < 2:
        return 1
    return fib2(num-1) + fib2(num-2)


for i in range(50):
    print fib2(i)
