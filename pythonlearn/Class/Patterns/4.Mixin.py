# -*- coding: utf-8 -*-
#


class FlyweightMixin(object):
    _instances = dict()

    def __init__(self, *args, **kargs):
        # 只想被继承不想被初始化
        raise NotImplementedException

    # 重载实例化触发的__new__
    def __new__(cls, *args, **kargs):
        return cls._instances.setdefault(
                    (cls, args, tuple(kargs.items())),
                    super(type(cls), cls).__new__(cls, *args, **kargs))


class Spam(FlyweightMixin):

    def __init__(self, a, b):
        self.a = a
        self.b = b


class Egg(FlyweightMixin):

    def __init__(self, x, y):
        self.x = x
        self.y = y

a = Spam(1, 2)
b = Spam(1, 2)
print  a is b
assert Egg('a', 'b') is Egg('a', 'b')
assert Spam(1, 2) is not Egg(1, 2)