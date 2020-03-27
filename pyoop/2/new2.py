""" 1. 有序的属性
2. 自引用
"""

import collections

class OrderdAttributes(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwargs):
        result = super().__new__(cls, name, bases, namespace)
        result._order = tuple( n for n in namespace if not n.startswith("__"))
        return result

class OrderdPreserved(metaclass=OrderdAttributes):
    pass


class Something(OrderdPreserved):
    hit = "1"
    def z(self):
        return False
    a = "a"
    b = "b"

s = Something()
print(s._order)






