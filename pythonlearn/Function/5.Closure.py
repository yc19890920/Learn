# -*- coding: utf-8 -*-


#######################################################################
# 1. 误区1
# 尽量避免在闭包中引用循环变量，或者后续会发生变化的变量。

# ------------------实例1----------------------
def count():
    funcs = []
    for i in [1, 2, 3]:
        def f():
            return i
        funcs.append(f)
    return funcs

f1, f2, f3 = count()
print f1(), f2(), f3()
# 3 3 3   ###不是期望的1，2，3
print f1.__closure__[0].cell_contents  # 打印闭包值 即i的值 3
# 为什么呢？原因在于上面的函数 f 引用了变量 i，但函数 f 并非立刻执行，当 for 循环结束时，此时变量 i 的值是3，funcs 里面的函数引用的变量都是 3，最终结果也就全为 3。

# 改进 1
def count():
    funcs = []
    for i in [1, 2, 3]:
        def g(param):
            f = lambda : param    # 这里创建了一个匿名函数
            return f
        funcs.append(g(i))        # 将循环变量的值传给 g
    return funcs
f1, f2, f3 = count()
print f1(), f2(), f3()
# 1 2 3
print f1.__closure__[0].cell_contents   # 打印闭包值 即i的值 1

# 改进 2  非闭包，没有引用自由变量 （嵌套函数必须引用一个外部的非全局的局部自由变量。）
def count():
    funcs = []
    for i in [1, 2, 3]:
        def g(j=i):     # 传参，初始化内部函数变量，外部遍历i已经传值给默认参数j了
            return j
        funcs.append(g)        # 返回内部函数
    return funcs

fs1 = count()
fs2 = count()
print f1(), f2(), f3()
# 1 2 3
print f1.__closure__
# None # 没有闭包，因为外部遍历i已经传值给默认参数j了


# ------------------实例2----------------------
# Python 延迟绑定

def multipliers():
    return [lambda x : i*x for i in range(4)]
# multipliers内嵌套一个匿名函数
# 该匿名函数引用外部非全局变量 i
# 返回该嵌套函数
print [m(2) for m in multipliers()]
# [6, 6, 6, 6]
"""
运行代码，代码从第62行开始运行，解释器碰到了一个列表解析，循环取multipliers()函数中的值，
而multipliers()函数返回的是一个列表对象，这个列表中有4个元素，每个元素都是一个匿名函数
（实际上说是4个匿名函数也不完全准确，其实是4个匿名函数计算后的值，因为后面for i 的循环不光循环了4次，
同时提还提供了i的变量引用，等待4次循环结束后，i指向一个值i=3,这个时候，匿名函数才开始引用i=3，计算结果。
所以就会出现[6,6,6,6]，因为匿名函数中的i并不是立即引用后面循环中的i值的，而是在运行嵌套函数的时候，才会查找i的值，这个特性也就是延迟绑定）

# 为了便于理解，你可以想象下multipliers内部是这样的(这个是伪代码，并不是准确的)：
def multipliers():
    return [lambda x: 3 * x, lambda x: 3 * x, lambda x: 3 * x, lambda x: 3 * x]

因为Python解释器，遇到lambda（类似于def）,只是定义了一个匿名函数对象，
并保存在内存中，只有等到调用这个匿名函数的时候，才会运行内部的表达式，
而for i in range(4) 是另外一个表达式，需等待这个表达式运行结束后，才会开始运行lambda 函数，此时的i 指向3，x指向2
"""

# 其实这个题目，可能目的是想输出：[0, 2, 4, 6]，如何改进才能输出这个结果呢？
def multipliers():
    # 添加了一个默认参数i=i
    return [lambda x, i=i: i*x for i in range(4)]
print [m(2) for m in multipliers()]
# [0, 2, 4, 6]

"""
那我们来看下，添加了一个i=i，到底发生了什么？

加了一个i=i后，就给匿名函数，添加了一个默认参数，
而python函数中的默认参数，是在python 解释器遇到def(i=i)或lambda 关键字时，就必须初始化默认参数，
此时for i in range(4)，每循环一次，匿名函数的默认参数i，
就需要找一次i的引用，i=0时，第一个匿名函数的默认参数值就是0，i=1时，第二个匿名函数的默认参数值就是1，以此类推。

# 为了便于理解，你可以想象下multipliers内部是这样的(这个是伪代码只是为了理解)：
def multipliers():
    return [lambda x,i=0: i*x, lambda x,i=1: i*x, lambda x,i=2: i*x, lambda x,i=3:i*x i=3]
# x的引用是2 所以output的结果就是：[0,2,4,6]


"""
# 当然你的i=i，也可以改成a=i。
def multipliers():
    return [lambda x, a=i: a * x for i in range(4)]

print [m(2) for m in multipliers()]
# [0, 2, 4, 6]
# Python的延迟绑定其实就是只有当运行嵌套函数的时候，才会引用外部变量i，不运行的时候，并不是会去找i的值，这个就是第一个函数，为什么输出的结果是[6,6,6,6]的原因。

import functools
def multipliers():
    return [functools.partial(lambda a, x: x * a, i) for i in range(4)]

print [m(2) for m in multipliers()]
# [0, 2, 4, 6]

#######################################################################
# 1. 误区2
### 禁止在闭包函数内对引用的自由变量进行重新绑定

# def foo(func):
#     free_value = 8
#     def _wrapper(*args, **kwargs):
#         old_free_value = free_value #保存旧的free_value
#         free_value = old_free_value * 2 #模拟产生新的free_value
#         func(*args, **kwargs)
#         free_value = old_free_value
#     return _wrapper

def foo(func):
    free_value = [8]
    def _wrapper(*args, **kwargs):
        old_free_value = free_value[0] #保存旧的free_value
        free_value[0] = old_free_value * 2 # 模拟产生新的free_value
        func(*args, **kwargs)
        return free_value[0]
    return _wrapper

def hello():
    print 'hello world'

hello = foo(hello)
i = hello()
print i
# 16
i = hello()
print i
# 32

def foo():
    free_value = [8]
    def _wrapper(*args, **kwargs):
        T = free_value[0]     # 保存旧的free_value
        free_value[0] = T * 2 # 模拟产生新的free_value
        return free_value[0]
    return _wrapper

f = foo()
print f()
print f()
print f()
# 16
# 32
# 64