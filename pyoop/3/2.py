class Fjs(object):
    def __init__(self, name):
        self.name = name

    def hello(self):
        print("said by : ", self.name)

    def __getattr__(self, item):
        print("访问了特性1：" + item)
        return None
        raise AttributeError

    def __setattr__(self, key, value):
        print("访问了特性2：" + key)
        self.__dict__[key] = value

    def __getattribute__(self, item):
        print("访问了特性3：" + item)
        return object.__getattribute__(self, item)


fjs = Fjs("fjs")
print(fjs.name )
print('-------------1-------')
fjs.hello()
print('--------------2------')
fjs.bb
"""
访问了特性：name
fjs
---------------2-----
访问了特性：hello
访问了特性：name
said by :  fjs
"""