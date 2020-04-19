# coding: utf-8

import functools

def add(a, b):
    return a + b

print add(4, 2)
# 6
plus3 = functools.partial(add, 3)
plus5 = functools.partial(add, 5)
print plus3(4)
# 7
print plus3(7)
# 10
print plus5(10)
# 15