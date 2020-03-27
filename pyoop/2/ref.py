""" 循环引用
"""
import weakref
class Parent(object):

    def __init__(self, *children):
        self.children = list(children)
        for child in self.children:
            # 循环引用
            # child.parent = self

            # 弱引用
            child.parent = weakref.ref(self)

    def __del__(self):
        print("Removing {__class__.__name__} {id:d}".format(
            __class__=self.__class__, id=id(self)
        ))

class Child(object):

    def __del__(self):
        print("Removing {__class__.__name__} {id:d}".format(
            __class__=self.__class__, id=id(self)
        ))


c1 = Child()
c2 = Child()
p = Parent( c1,c2 )
import gc
print(gc.collect())
print(gc.garbage)
print('--------------')
print(id(p), id(c1), id(c2))
# del c1
# del c2
print(p)
del p
print('--------------')
print(gc.collect())
print(gc.garbage)
print('-------------------')


