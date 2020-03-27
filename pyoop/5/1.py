
import collections.abc

class Power(collections.abc.Callable):

    def __call__(self, x, n):
        if n==0:
            return 1
        elif n%2==1:
            return self.__call__(x, n-1)*x
        else:
            t = self.__call__(x, n//2)
            return t*t

# p = Power()

class Power2(collections.abc.Callable):

    _caches = {}

    def __call__(self, x, n):
        if (x, n) not in self._caches:
            if n==0:
                self._caches[x,n] = 1
            elif n%2==1:
                self._caches[x,n] = self.__call__(x, n-1)*x
            else:
                t = self.__call__(x, n//2)
                self._caches[x,n] = t*t
        return self._caches[x,n]
# p = Power2()
# print(p(5,20))

from functools import lru_cache
@lru_cache(maxsize=128)
def power(x, n):
    if n==0:
        return 1
    elif n%2==1:
        return power(x, n-1)*x
    else:
        t = power(x, n//2)
        return t*t

# print(power(5,20))

import timeit

it1 = timeit.timeit("power(2, 128)", """
from functools import lru_cache
@lru_cache(maxsize=5)
def power(x, n):
    if n==0:
        return 1
    elif n%2==1:
        return power(x, n-1)*x
    else:
        t = power(x, n//2)
        return t*t
""", number=1000000)

it2 = timeit.timeit("p(2, 1024)", """
import collections.abc
class Power2(collections.abc.Callable):

    _caches = {}

    def __call__(self, x, n):
        if (x, n) not in self._caches:
            if n==0:
                self._caches[x,n] = 1
            elif n%2==1:
                self._caches[x,n] = self.__call__(x, n-1)*x
            else:
                t = self.__call__(x, n//2)
                self._caches[x,n] = t*t
        return self._caches[x,n]
p = Power2()
""", number=1000000)

print(it1, it2)


