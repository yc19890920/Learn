
# 设计模式

## 《Design Patterns》一书把设计模式分为了3大类：
1. 创建型模式（creational pattern）
2. 结构型模式（structural pattern）
3. 行为型模式（behavioral patterns）


## 一. 创建型模式（creational pattern）
```
对类的实例化过程进行了抽象，能够使软件模块做到与对象创建和组织的无关性。
为了使体系结构更加清晰，一些软件在设计上要求当创建类的具体实例时，能够根据具体的语境来动态地决定怎样创建对象，
创建哪些对象，以及怎样组织和表示这些对象，而创建型模式所要描述的就是该如何来解决这些问题。
```
> 创建型模式包括以下几种：
>> 1、Simple Factory模式
>> 专门定义一个类来负责创建其它类的实例，被创建的实例通常都具有共同的父类。

>> 2、Factory Method工厂模式
>> 将对象的创建交由父类中定义的一个标准方法来完成，而不是其构造函数，究竟应该创建何种对象由具体的子类负责决定

>> 3、Abstract Factory模式
>> 提供一个共同的接口来创建相互关联的多个对象。

>> 4、Builder模式
>> 将复杂对象的创建同它们的具体表现形式（representation）区别开来，这样可以根据需要得到具有不同表现形式的对象。

>> 5、Singleton模式
>> 保证系统只会产生该类的一个实例，同时还负责向外界提供访问该实例的标准方法。

>> 6、Prototype模式
>> 利用一个能对自身进行复制的类，使得对象的动态创建变得更加容易。


### 文档
- [Python 设计模式: 工厂模式(factory pattern)](https://mozillazg.github.io/2016/08/python-factory-pattern.html)
- [Python 设计模式: 建造者模式(builder pattern)](https://mozillazg.github.io/2016/08/python-builder-pattern.html)
- [python多线程下保持单例模式的实例唯一](http://xiaorui.cc/2016/04/10/python%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%B8%8B%E4%BF%9D%E6%8C%81%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F%E7%9A%84%E5%AE%9E%E4%BE%8B%E5%94%AF%E4%B8%80/)
- [Python 设计模式: 原型模式(prototype pattern)](https://mozillazg.github.io/2016/09/python-prototype-pattern.html)


## 二. 结构型模式（structural pattern）

>> 1、The Adapter Pattern(适配器模式: 解决接口不兼容问题)

>> 2、The Decorator Pattern(装饰器模式： 无需子类化实现扩展对象功能问题)

>> 3、The Facade Pattern(外观模式: 简化复杂对象的访问问题)

>> 4、The Flyweight Pattern(享元模式: 实现对象复用从而改善资源使用)

>> 5、The Model-View-Controller Pattern(mvc模式：解耦展示逻辑和业务逻辑)

>> 6、The Proxy Pattern(代理模式：通过一层间接保护层实现更安全的接口访问）

### 文档
- [Python适配器模式](http://blog.csdn.net/duxu24/article/details/72847523)
- [Python修饰器模式](http://blog.csdn.net/duxu24/article/details/72859918)
- [python中的享元模式(flyweight)](https://fanchao01.github.io/blog/2015/04/13/python-flyweight/)
- [python设计模式之享元模式](http://dongweiming.github.io/python-flyweight.html)


## 三. 行为型模式（behavioral patterns）

>> 1、The Chain of Responsibility Pattern (责任链模式:创建链式对象用来接收广播消息)

>> 2、The Command Pattern(命令模式：用来给应用添加Undo操作)

>> 3、The Interpreter Pattern(解释器模式：用来实现Domain Specific Language(DSL))

>> 4、The Observer Pattern(发布订阅模式：用来处理多个对象之间的发布订阅问题)

>> 5、The State Pattern(状态模式：实现有限状态机)

>> 6、The Strategy Pattern(策略模式：动态选择算法策略)

>> 7、The Template Pattern(模板模式：抽象出算法公共部分从而实现代码复用)

### 文档
- [python设计模式之桥接模式](http://dongweiming.github.io/python-bridge.html)
- [python设计模式之观察者模式](http://dongweiming.github.io/python-observer.html)

- [python设计模式之命令调度模式](http://dongweiming.github.io/python-command.html)
- [12.11 实现消息发布/订阅模型](http://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p11_implement_publish_subscribe_messaging.html)
- [python设计模式之状态模式](http://dongweiming.github.io/python-state.html)
- [python设计模式之策略模式](http://dongweiming.github.io/python-strategy.html)


####  
- [用python实现设计模式](http://python-web-guide.readthedocs.io/zh/latest/design/design.html)
- [python实践设计模式](http://www.uml.org.cn/sjms/201305283.asp)
- [Python设计模式1-创建型模式](http://www.jianshu.com/p/2450b785c329)