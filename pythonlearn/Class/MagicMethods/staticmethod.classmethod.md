

## 文档
- [Python 中的 classmethod 和 staticmethod 有什么具体用途？](https://www.zhihu.com/question/20021164)
- [Difference between @staticmethod and @classmethod in Python](http://pythoncentral.io/difference-between-staticmethod-and-classmethod-in-python/)
- [PYTHON中STATICMETHOD和CLASSMETHOD的差异](http://www.wklken.me/posts/2013/12/22/difference-between-staticmethod-and-classmethod-in-python.html)
- [python学习之self，cls，staticmethod，classmethod](http://www.cnblogs.com/zmlctt/p/4224633.html)
- [python 类的实例方法，静态方法，类方法辨析和实例讲解](http://blog.csdn.net/a447685024/article/details/52424481)


## 说明
> 类的方法有三种：
>> 1. 实例方法：通过def定义的 普通的一般的，需要至少传递一个参数，一般用self，这样的方法必须通过一个类的实例去访问，类似于c++中通过对象去访问；
>> 2. 类方法：在def前面加上@classmethod，这种类方法的一个特点就是可以通过类名去调用，但是也必须传递一个参数，一般用cls表示class，表示可以通过类直接调用；
>> 3. 静态方法： 在def前面加上@staticmethod，这种类方法是静态的类方法，类似于c++的静态函数，他的一个特点是参数可以为空，同样支持类名和对象两种调用方式；

```
普通的方法，第一个参数需要是self，它表示一个具体的实例本身。
如果用了staticmethod，那么就可以无视这个self，而将这个方法当成一个普通的函数使用。
而对于classmethod，它的第一个参数不是self，是cls，它表示这个类本身。
```

## 作用

```
一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。
而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。
这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。

既然@staticmethod和@classmethod都可以直接类名.方法名()来调用，那他们有什么区别呢
从它们的使用上来看,
---- @staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
---- @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。
而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。
```

```
# -*- coding: utf-8 -*-

class A(object):

    def __init__(self):
        pass

    def foo1(self):
        print "Hello", self

    @staticmethod
    def foo2():
        print "hello"

    @classmethod
    def foo3(cls):
        print "hello",cls

a = A()
a.foo1()   # 最常见的调用方式，但与下面的方式相同
# Hello <__main__.A object at 0x00000000027E8080>
A.foo1(a)  # 这里传入实例a，相当于普通方法的self
# Hello <__main__.A object at 0x00000000027E8080>

a.foo2()
# hello

a.foo3()
# hello <class '__main__.A'>


A.foo2()           # 这里，由于静态方法没有参数，故可以不传东西
# hello

A.foo3()           # 这里，由于是类方法，因此，它的第一个参数为类本
# hello <class '__main__.A'>

print A           # 可以看到，直接输入A，与上面那种调用返回同样的信息。
# <class '__main__.A'>
```
