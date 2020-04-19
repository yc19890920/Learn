# -*- coding: utf-8 -*-


import itertools

for i in itertools.count(start=10, step=3):
    print i,
    if i > 100:
        break

# 10 13 16 19 22 25 28 31 34 37 40 43 46 ...

n = itertools.cycle('ABCD')
# A B C D A B C D ...

print '\n'
for i in itertools.repeat('ABCD', times=5):
    print i,
# ABCD ABCD ABCD ABCD ABCD

print '\n'
for i in itertools.compress('ABCDEF', [1,0,1,0,1]):
    print i,
# A C E

print '\n'
for i in itertools.ifilterfalse(lambda x: x%2, range(10)):
    print i,
# 0 2 4 6 8

print '\n'
for i in itertools.islice('ABCDEFG', 2, None, 2):
    print i,
# C E G

print '\n'
for i in itertools.tee([1,2,3,4], ):
    for x in i:
        print x,

print '\n'
for i in itertools.izip_longest('ABCD', 'xy', fillvalue='-'):
    print i,

print '\n'
a = (1,2,3)
b = ('A','B')
c = itertools.product(a,b)
for i in c:
    print(i)
# (1, 'A')
# (1, 'B')
# (2, 'A')
# (2, 'B')
# (3, 'A')
# (3, 'B')

print '\n'
for i in itertools.product(range(2), repeat=2):
    print(i)
# (0, 0)
# (0, 1)
# (1, 0)
# (1, 1)

print '\n'
a = [1, 2, 3, 4]
s = [i for i in itertools.permutations(a, 3)] # 从序列a中选出3个元素进行排列
print s

print '\n'



