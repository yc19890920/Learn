import collections.abc
import math

class StatList(list):
    """  主动计算，数据量规模大时，提升性能
    继承列表，改变一些和常量
    """

    def __init__(self, *args, **kwargs):
        self.sum0 = 0 # len(self)
        self.sum1 = 0 # sum(self)
        self.sum2 = 0 # sum(x**2 for x in self)
        super().__init__(*args, **kwargs)
        for x in self:
            self._new(x)

    def _new(self, value):
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value*value

    def _rmv(self, value):
        self.sum0 -= 1
        self.sum1 -= value
        self.sum2 -= value*value

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__setitem__(index, value)
            for x in olds:
                self._rmv(x)
            for x in value:
                self._new(x)
        else:
            old = self[index]
            super().__setitem__(index, value)
            self._rmv(old)
            self._new(value)
        # value1 = super().__getitem__(index)
        # super().__setitem__(index, value)
        # self._rmv(value1)
        # self._new(value)

    def __delitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__delitem__(index)
            for x in olds:
                self._rmv(x)
        else:
            old = self[index]
            super().__delitem__(index)
            self._rmv(old)
        # value1 = super().__getitem__(index)
        # super().__delitem__(index)
        # self._rmv(value1)

    def __iter__(self):
        i = 0
        try:
            while True:
                v = self[i]
                yield v
                i += 1
        except IndexError:
            return

    def insert(self, index, value):
        super().insert(index, value)
        self._new(value)

    def append(self, value):
        super().append(value)
        self._new(value)

    def extend(self, values):
        for v in values:
            self.append(v)

    def clear(self):
        'S.clear() -> None -- remove all items from S'
        try:
            while True:
                self.pop()
        except IndexError:
            pass
        finally:
            self.sum0 = 0
            self.sum1 = 0
            self.sum2 = 0

    def pop(self, index=0):
        value = super().pop(index)
        self._rmv(value)

    def remove(self, value):
        super().remove(value)
        self._rmv(value)

    def __iadd__(self, values):
        self.extend(values)
        return self

    @property
    def mean(self):
        """ 计算平均数 """
        return self.sum0 and self.sum1/self.sum0 or 0

    @property
    def stdev(self):
        """ 计算标准差 """
        return ( self.sum1 and math.sqrt(self.sum0*self.sum2 - self.sum1*self.sum1)/self.sum1 or 0 )

# s1 = StatList()
# print(s1.stdev)

s = StatList([2,4,3,4,5,5,7,9,10])
print(s.sum0, s.sum1, s.sum2, s.mean, s.stdev, s)

s[2] =4
print(s.sum0, s.sum1, s.sum2, s.mean, s.stdev, s)

del s[-1]
print(s.sum0, s.sum1, s.sum2, s.mean, s.stdev, s)

s.pop(-1)
print(s.sum0, s.sum1, s.sum2, s.mean, s.stdev, s)

print(s[:2])

for i in s:
    print(i, end=",")

