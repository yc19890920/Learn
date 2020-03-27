
class DotDict(dict):
    '''用于操作 dict 对象

    # >>> dd = DotDict(a=1, b=2)
    # >>> dd.c = 3
    # >>> dd
    # {'a': 1, 'c': 3, 'b': 2}
    # >>> del dd.c
    # >>> dd
    # {'a': 1, 'b': 2}
    '''

    Fields = tuple()

    def __getitem__(self, item):
        value = dict.__getitem__(self, item)
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        return value

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    __getattr__ = __getitem__
    # __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


d = DotDict(a=1, b=2)
print(d)

d.a = 2
d.b = 3
d.d = 4
print(d)

