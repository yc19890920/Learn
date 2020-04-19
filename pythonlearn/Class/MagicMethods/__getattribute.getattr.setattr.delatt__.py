# -*- coding: utf-8 -*-


# 利用__getattr__和setattr缓存
class Cache(object):

    def __setattr__(self, name, value):
        '''''
        @summary: 每当属性被赋值的时候都会调用该方法，因此不能再该方法内赋值 self.name = value 会死循环
        '''
        self.__dict__[name] = 'T-{}'.format(value)

    def __getattr__(self, real_name):
        '''''
        @summary: 当访问不存在的属性时会调用该方法
        '''
        print 'through getattr to get attribute %r' % real_name
        # value = str(real_name)
        value = None
        setattr(self, real_name, value)  # 调用 __setattr__
        return value

    def __delattr__(self,name):
        '''''
        @summary: 当删除属性时调用该方法
        '''
        print "__delattr__:Delect attribute '%s'"%name
        del self.__dict__[name]


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


delattr(cache, 'a')
print cache.__dict__
{'b': 'T-123'}