# -*- coding: utf-8 -*-
"""
在python中使用内置方法对列表进行排序可以使用两种方法：
一种是列表提供的sort方法，该方法的特性是在原址进行排序，没有生成新的列表。
还有一种是python提供的内置方法sorted()，该方法接受一个序列，并返回一个排序好的序列，这种方式没有改变原序列的排序。
这里测试，使用的是list提供的sort内置方法。也就是原址排序。
在上面所列举的排序方式中，list内置方法排序所用时间是最短的，说明性能是最好的，至于其内部实现方式，需要看源码才能明白。

    sort是容器的函数：sort(cmp=None, key=None, reverse=False)
    sorted是Python的内建函数：sorted(iterable, cmp=None, key=None, reverse=False)   # iterable指定要排序的list或者iterable，不用多说；
    cmp：比较函数，比较什么参数由key决定。例如：cmp(e1, e2) 是具有两个参数的比较函数，返回值：负数（e1 < e2）；0（e1 == e2）；正数（ e1 > e2）。
    key：用列表元素的某个属性或函数作为关键字。
    reverse：排序规则，可以选择True或者False。
    sorted多一个参数iterable：待排序的可迭代类型的容器

Python中的sorted函数以及operator.itemgetter函数
operator模块提供的itemgetter函数用于获取对象的哪些维的数据，参数为一些序号（即需要获取的数据在对象中的序号)，下面看例子。
a = [1,2,3]
>>> b=operator.itemgetter(1)      //定义函数b，获取对象的第1个域的值
>>> b(a)
2
>>> b=operator.itemgetter(1,0)   //定义函数b，获取对象的第1个域和第0个的值
>>> b(a)
(2, 1)
要注意，operator.itemgetter函数获取的不是值，而是定义了一个函数，通过该函数作用到对象上才能获取值。
sorted是Python的内建函数：sorted(iterable, cmp=None, key=None, reverse=False)
参数解释：
（1）iterable指定要排序的list或者iterable，不用多说；
（2）cmp为函数，指定排序时进行比较的函数，可以指定一个函数或者lambda函数，如：
       students为类对象的list，没个成员有三个域，用sorted进行比较时可以自己定cmp函数，例如这里要通过比较第三个数据成员来排序，代码可以这样写：
        students = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
       sorted(students, key=lambda student : student[2])
（3）key为函数，指定取待排序元素的哪一项进行排序，函数用上面的例子来说明，代码如下：
       sorted(students, key=lambda student : student[2])
       key指定的lambda函数功能是去元素student的第三个域（即：student[2]），因此sorted排序时，会以students所有元素的第三个域来进行排序。
有了上面的operator.itemgetter函数，也可以用该函数来实现，例如要通过student的第三个域排序，可以这么写：
sorted(students, key=operator.itemgetter(2))
sorted函数也可以进行多级排序，例如要根据第二个域和第三个域进行排序，可以这么写：
sorted(students, key=operator.itemgetter(1,2))
"""

if __name__ == "__main__":
    list1 = [1, 3, 2, 5, 4]
    list1.sort()
    print list1
    # [1, 2, 3, 4, 5]

    # 基于key函数排序
    list1=[(8, 'Logan', 20), (2, 'Mike', 22), (5, 'Lucy', 19)]
    list1.sort(key=lambda x:x[0])
    print list1
    # [(8, 'Logan', 20), (5, 'Lucy', 19), (2, 'Mike', 22)]

    # 基于cmp函数
    list1=[(8, 'Zogan', 20), (2, 'Mike', 22), (5, 'Lucy', 19)]
    list1.sort(cmp=lambda x,y: cmp(x[2],y[2]))
    print list1
    # [(5, 'Lucy', 19), (8, 'Zogan', 20), (2, 'Mike', 22)]

    # 基于reverse函数
    list1=[(8, 'Zogan', 20), (2, 'Mike', 22), (5, 'Lucy', 19)]
    list1.sort(key=lambda x:x[0], reverse=True)
    print list1
    # [(8, 'Zogan', 20), (5, 'Lucy', 19), (2, 'Mike', 22)]

    ############################################################
    # Python中的sorted函数以及operator.itemgetter函数
    import operator
    students = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
    t = sorted(students, key=operator.itemgetter(1), reverse=True) # 用第一个域的值 即"A" 做为排序函数, 倒序
    print t
    # [('jane', 'B', 12), ('dave', 'B', 10), ('john', 'A', 15)] # B -> B -> A

    students = [('john', 'A', [10, 20]), ('jane', 'B', [10, 22]), ('dave', 'B', [10, 18])]
    t = sorted(students, key=operator.itemgetter(2, 1), reverse=True) # 用第二个域的值（列表），列表里面下标为1 进行排序, 倒序
    print t
    [('jane', 'B', [10, 22]), ('john', 'A', [10, 20]), ('dave', 'B', [10, 18])] # 22 -> 20 -> 18

    ############################################################
    # python 字典排序
    # dic.iteritems() 得到[(键，值)]的列表。然后用sorted方法，通过key这个参数，指定排序是按照value，也就是第一个元素d[1的值来排序。
    # reverse = True表示是需要翻转的，默认是从小到大，翻转的话，那就是从大到小。
    dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
    dic2 = sorted(dic.iteritems(), key=lambda d:d[1], reverse=True)
    print dic2
    # [('aa', 74), ('a', 31), ('bc', 5), ('asd', 4), ('c', 3), ('d', 0)]

    dic2 = sorted(dic.iteritems(), key=operator.itemgetter(1), reverse=False)
    print dic2
    # [('d', 0), ('c', 3), ('asd', 4), ('bc', 5), ('a', 31), ('aa', 74)]





