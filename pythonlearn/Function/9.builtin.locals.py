# coding: utf-8


def t(a, b=1):
    print locals()
    # {'a': 1, 'b': 1}
    print 'a: {a}, b: {b}'.format(**locals())
    # a: 1, b: 1
    print a+b
    # 2

t(1)


##############################
def t(a, b=1):
    print locals()
    # {'a': 1, 'b': 3}
    print 'a: {a}, b: {b}'.format(**locals())
    # a: 1, b: 2
    # a: 1, b: 3
    print a+b
    # 4

t(1,3)

##############################
def t(a, b=1):
    b = 2
    print locals()
    # {'a': 1, 'b': 2}
    print 'a: {a}, b: {b}'.format(**locals())
    print a+b
    # 3

t(1,3)


