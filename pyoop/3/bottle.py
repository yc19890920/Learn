import functools
class lazy_attribute(object):
    """ A property that caches itself to the class object. """

    def __init__(self, func):
        functools.update_wrapper(self, func, updated=[])
        self.getter = func

    def __get__(self, obj, cls):
        value = self.getter(cls)
        setattr(cls, self.__name__, value)
        return value

class Widget(object):
    @lazy_attribute
    def complex_attr_may_not_need(clz):
        print('complex_attr_may_not_need is needed now')
        return sum(i*i for i in range(1000000))

if __name__ == '__main__':
    print(Widget.__dict__.get('complex_attr_may_not_need'))  # <__main__.lazy_attribute object at 0x02B12450>
    Widget.complex_attr_may_not_need                        # complex_attr_may_not_need is needed now
    print(Widget.__dict__.get('complex_attr_may_not_need'))  # 332833500

    print(sum(i*i for i in range(1000000)))