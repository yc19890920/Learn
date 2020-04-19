

在Python中，如果我们想实现创建类似于序列和映射的类，可以通过重写魔法方法__getitem__、__setitem__、__delitem__、__len__方法去模拟。

__xxxitem__:使用 [''] 的方式操作属性时被调用

__setitem__:每当属性被赋值的时候都会调用该方法，因此不能再该方法内赋值 self.name = value 会死循环

__getitem__:当访问不存在的属性时会调用该方法

__delitem__:当删除属性时调用该方法



````
class A(object):  
    def __init__(self):  
        self['B'] = "BB"  
        self['D'] = "DD"  
        del self['D']  
      
    def __setitem__(self,name,value):  
        ''''' 
        @summary: 每当属性被赋值的时候都会调用该方法，因此不能再该方法内赋值 self.name = value 会死循环 
        '''  
        print "__setitem__:Set %s Value %s"%(name,value)  
        self.__dict__[name] = value  
      
    def __getitem__(self,name):  
        '''''  
        @summary: 当访问不存在的属性时会调用该方法 
        '''  
        print "__getitem__:No attribute named '%s'"%name  
        return None  
      
    def __delitem__(self,name):  
        '''''  
        @summary: 当删除属性时调用该方法 
        '''  
        print "__delitem__:Delect attribute '%s'"%name  
        del self.__dict__[name]  
        print self.__dict__  
      
      
if __name__ == "__main__":  
    X = A()  
    b = X['bb']  
    
    
    
__setitem__:Set B Value BB
__setitem__:Set D Value DD
__delitem__:Delect attribute 'D'
{'B': 'BB'}
__getitem__:No attribute named 'bb'
````

## 文档
- [Python的魔法函数之 - \__len__,\__getitem__,\__setitem__,\__delitem__](http://www.cnblogs.com/wancy86/p/6235713.html)