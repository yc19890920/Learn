# -*- coding: utf-8 -*-

"""
形如
aa=[1,2,2,3,2,4]
bb=[1,4,5]
重复的元素：[1,4,]
"""

# 方法一： set
aa=[1,2,2,3,2,4]
bb=[1,4,5]

print list(set(aa)&set(bb))

# 方法二：字典
cc = []
dd = dict((i, 1) for i in aa)
for i in bb:
    if dd.get(i) is not None:
        cc.append(i)
print cc

# 方法三：列表推导式
cc=[v for v in aa if v in bb]
print cc


