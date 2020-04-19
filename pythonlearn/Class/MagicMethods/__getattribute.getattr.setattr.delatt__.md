

## __getattr__/__setattr__/__delattr__

**使用这三个方法你可以随时修改、删除、添加类属性或值，是不是觉得大吃一惊？**

拦截对象的所有特性访问是可能的，这样可以用旧式类实现属性。
为了在访问特性时可以执行代码，必须使用一些魔法方法：（在旧式类中只需要后3个）

- （1）\__getattribute__(self, name)：当特性name被访问时自动被调用（只能在新式类中使用）；

- （2）\__getattr__(self, name)：当特性name被访问且对象没有相应的特性时被自动调用； （用于获取不存在的属性 obj.attr）

- （3）\__setattr__(self, name, value)：当试图给name赋值时会被自动调用；

- （4）\__delattr__(self, name)：当试图删除特性name时被自动调用；


### 利用__getattr__和setattr缓存

```
# 利用__getattr__和setattr缓存
class Cache(object):
    # def __setattr__(self, name, value):
    #     pass

    def __getattr__(self, real_name):
        print 'through getattr to get attribute %r' % real_name
        value = str(real_name)
        setattr(self, real_name, value)
        return value


cache = Cache()

print cache.__dict__
# {}

print cache.a
# through getattr to get attribute 'a'
# a

print cache.__dict__
# {'a':'a'}

print cache.a
# a

setattr(cache, 'b', 123)
print cache.__dict__
# {'a': 'a', 'b': 123}
```


### 文档
- [Python魔法方法之属性访问 ( \__getattr__, \__getattribute__, \__setattr__, \__delattr__ )](http://www.cnblogs.com/Jimmy1988/p/6804095.html)
- [python \__setattr__, \__getattr__, \__delattr__, \__call__](http://www.cnblogs.com/coder2012/p/4309999.html)