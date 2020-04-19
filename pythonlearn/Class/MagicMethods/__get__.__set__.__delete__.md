什么是描述符

Python 2.2 引进了 Python 描述符，同时还引进了一些新的样式类，但是它们并没有得到广泛使用。
Python 描述符是一种创建托管属性的方法。描述符具有诸多优点，诸如：保护属性不受修改、属性类型检查和自动更新某个依赖属性的值等。

说的通俗一点，从表现形式来看，一个类如果实现了 \__get__,\__set__,\__del__方法(三个方法不一定要全部都实现)，
并且该类的实例对象通常是另一个类的类属性，那么这个类就是一个描述符。

\__get__,\__set__,\__del__的具体声明如下：

> __get__(self, instance, owner)
> __set__(self, instance, value)
> __delete__(self, instance)

其中：

> \_get__ 用于访问属性。它返回属性的值，或者在所请求的属性不存在的情况下出现 AttributeError 异常。类似于javabean中的get。
> \__set__ 将在属性分配操作中调用。不会返回任何内容。类似于javabean中的set。
> \__delete__ 控制删除操作。不会返回内容。

注意：

只实现__get__方法的对象是非数据描述符，意味着在初始化之后它们只能被读取。而同时实现__get__和__set__的对象是数据描述符，意味着这种属性是可读写的。   

3、为什么需要描述符

因为Python是一个动态类型解释性语言，不像C/C++等静态编译型语言，数据类型在编译时便可以进行验证，而Python中必须添加额外的类型检查逻辑代码才能做到这一点，这就是描述符的初衷。



**property**

前面提到过使用定义类的方式使用描述符，但是如果每次为了一个属性都单独定义一个类，有时将变得得不偿失。
为此，python提供了一个轻量级的数据描述符协议函数Property()，其使用装饰器的模式，可以将类方法当成属性来访问。它的标准定义是:

**property(fget=None,fset=None,fdel=None,doc=None) **

前面3个参数都是未绑定的方法，所以它们事实上可以是任意的类成员函数，分别对应于数据描述符的中的__get__，__set__，__del__方法，所以它们之间会有一个内部的与数据描述符的映射。

property有两种使用方式，一种是函数模式，一种是装饰器模式。

### 函数模式
```
class test(object):

    def __init__(self):
        self._x = None

    def getx(self):
        print("get x")
        return self._x

    def setx(self, value):
        print("set x")
        self._x = value

    def delx(self):
        print("del x")
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")

T = test()

T.x = 1
print T.x
# set x
# get x
# 1
```

### 饰器模式
```
class test(object):

    def __init__(self):
        self.__x = None

    @property
    def x(self):
        print("get x")
        return self.__x

    @x.setter
    def x(self, value):
        print "set x"
        self.__x = value

    @x.deleter
    def x(self):
        print "del x"
        del self.__x

T1 = test()

T1.x = 1
print T1.x
# set x
# get x
# 1
```

** 注意：三个函数的名字(也就是将来要访问的属性名)必须一致。**