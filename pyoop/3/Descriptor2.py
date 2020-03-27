class C(object):
    a = 'abc'
    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        return object.__getattribute__(self, *args, **kwargs)
    #    return "haha"
    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"

    def __get__(self, instance, owner):
        print("__get__() is called", instance, owner)
        return self

    def foo(self, x):
        print(x)

class C2(object):
    d = C()

if __name__ == '__main__':
    c = C()
    c2 = C2()
    print(c.a)
    print(c.zzzzzzzz)
    c2.d
    print(c2.d.a)