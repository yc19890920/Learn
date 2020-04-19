

## 定义
> - 全局变量
>> 在模块内、在所有函数外面、在class外面，这就是全局变量
> - 局部变量
>> 在函数内、在class的方法内（未加self修饰），这就是局部变量
> - 静态变量
>> 在class内的，但不在class的方法内的，这就是静态变量
> - 实例变量
>> 在class的方法内的，用self修饰的变量，这就是实例变量

## 要点总结

1、类变量可以用 类名.类变量 和 self.类变量 两种方式访问，后者一般情况不建议使用。

2、类变量是所有对象所共享的，无论任何时候都建议用类名的方式访问类变量。

3、实例变量在类内部用 self 访问，在类外部用实例名访问。

4、类变量通过 self 访问时则被转化为实例变量，被绑定到特定的实例上，其值会屏蔽掉类变量。

5、通过对实例变量（self）的形式对类变量重新赋值后，类变量的值不随之变化。

6、方法内的局部变量会屏蔽掉类变量和实例变量。

7、同一实例变量在不同的实例中可能拥有不同的值。



## 文档
- [Python 类中的"静态"成员变量](http://www.cnblogs.com/turtle-fly/p/3280610.html)
- [python变量（全局变量，局部变量，类变量，实例变量）](http://www.imooc.com/article/14652)
- [Static class variables in Python](https://stackoverflow.com/questions/68645/static-class-variables-in-python)