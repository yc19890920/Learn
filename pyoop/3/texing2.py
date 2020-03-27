""" 主动计算属性
定义很多特性的setter来达到目的，明显多余。
扩展dict类型即可

- dict类型使用__init__()方法完成字典值的填充，然后判断是否提供了足够的初始化数据。使用了\__setattr__()函数来为字典添加新项，每当属性的赋值操作发生时就会调用_solve()函数。
- 在\__getattr__()函数中，使用None来标识属性的缺失。

self.distance = self.rate*self.time
"""


class RateTimeDistance(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._solve()

    def __getattr__(self, item):
        # print('--------2---------')
        return self.get(item, None)

    def __setattr__(self, key, value):
        self[key] = value
        self._solve()

    def __getattribute__(self, item):
        # print('--------1---------')
        if item.startswith("__"): raise AttributeError
        return object.__getattribute__(self, item)

    def __dir__(self):
        return list(self.keys())

    def _solve(self):
        if self.rate is not None and self.time is not None:
            self["distance"] = self.rate*self.time
            # self.distance = self.rate*self.time
        elif self.rate is not None and self.distance is not None:
            self["time"] = self.distance/self.rate
        elif self.time is not None and self.distance is not None:
            self["rate"] = self.distance/self.time

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass

    def __delete__(self, instance):
        pass

r = RateTimeDistance()
r.time = 9.5
print(r)

r.rate = 6.24
print(r)
print(r.distance)
print(r.distance1)
# r.__dict__["aa"] = 1
# print(r)




class BlackJackCard(object):
    """ Abstract SuperClass
    """

    def __init__(self, rank, suit, hard, soft):
        super().__setattr__('rank', rank)
        super().__setattr__('suit', suit)
        super().__setattr__('hard', hard)
        super().__setattr__('soft', soft)

    def __str__(self):
        return "{0.rank}{0.suit}".format(self)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError(
                "'{__class__.__name__}' cannot set '{key}'".format(
                 __class__=self.__class__, key=key))
        raise AttributeError(
            "'{__class__.__name__}' has no attribute '{key}'".format(
             __class__=self.__class__, key=key))

    def __getattribute__(self, item):
        if item.startswith("__"): raise AttributeError
        return object.__getattribute__(self, item)


b = BlackJackCard('A', "♣", 1, 11)
# b.rank = 1


