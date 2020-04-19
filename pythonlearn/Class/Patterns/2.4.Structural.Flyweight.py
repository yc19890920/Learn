# -*- encoding: utf-8 -*-

# instances是闭包，好懂吧
def flyweight(cls):
    instances = dict()
    return lambda *args, **kargs: instances.setdefault(
        (args, tuple(kargs.items())),
        cls(*args, **kargs)
    )


@flyweight
class Spam(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b


@flyweight
class Egg(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


assert Spam(1, 2) is Spam(1, 2)
assert Spam(1, 2) is not Spam(3, 4)
assert Egg('a', 'b') is Egg('a', 'b')
assert Spam(1, 2) is not Egg(1, 2)
