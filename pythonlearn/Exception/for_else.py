# -*- coding: utf-8 -*-

"""
for语句是python中的循环控制语句。
可用来遍历某一对象，还具有一个附带的可选的else块，主要用于处理for语句中包含的break语句。
如果for循环未被break终止，则执行else块中的语句。
break 在需要时终止for循环
continue 跳过位于其后的语句，开始下一轮循环。

即在for 循环中，如果没有从任何一个break中退出，则会执行和for对应的else
只要从break中退出了，则else部分不执行。


没有else语句的话，你需要设置一个标志，然后在后面对其检测，以此确定是否存在满足条件的值。
condition_is_met = False
for x in data:
    if meets_condition(x):
        condition_is_met = True

if not condition_is_met:
    # raise error or do additional processing

这不是一个真正重要的东西，而在许多其他语言中你必须要如此做。
但是类似Python的许多其他特性，else语句可以生成更加优雅的Python风格的（Pythonic）代码。
毫无疑问，上面的例子中，使用else语句使得代码更加The Zen of Python友好：
"""

for x in xrange(10):
    if x==100:
        break
    # if x==3:
    #     break
    print '-------', x
else:
    print 'process...'