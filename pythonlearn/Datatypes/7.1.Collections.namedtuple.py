# -*- coding:utf-8 -*-

from collections import namedtuple

P = namedtuple('Point', ['x', 'y'], verbose=False)

p = P(11, y=22)
# print p.x



datas = [
    ('Tom', 15),
    ('Lily', 18),
    ('Alax', 13),
]

U = namedtuple("User", ["name", "age"], verbose=True)
for d in map(U._make, datas):
    print d.age