

class TypedProperty(object):

    def __init__(self, name, type, default=None):
        self.name = "_" + name
        self.type = type
        self.default = default if default else type()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Must be a %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self,instance):
        raise AttributeError("Can't delete attribute")

class Foo(object):
    name = TypedProperty("name", str)
    num = TypedProperty("num", int, 42)

acct = Foo()
acct.name = "obi"
acct.num = 1234
print acct.num
# 1234
print acct.name
# obi

# trying to assign a string to number fails
# acct.num = '1234'
# TypeError: Must be a <type 'int'>


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
# 1


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


