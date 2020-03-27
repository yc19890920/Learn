"""
创建非数据修饰符： 修饰符对象包含或获取数据
1. 使用__get__()、__set__()
2. 不使用__get__()


拥有者类实例包含数据：
@property

拥有者包含数据：
@staticmethod、@classmethod
"""

# 1. 非数据修饰符类
# 由于非数据修饰符不包含__get__()函数，也没有返回内部数值，因此只能直接访问元素个数值来获得数据。
class UnitValue(object):
    """ Measure and Unit conbind"""

    def __init__(self, unit):
        self.value = None
        self.unit = unit
        self.defualt_fomat = "5.2f"

    def __set__(self, instance, value):
        print('--------1---------')
        print(self, instance, value)
        self.value = value

    def __str__(self):
        return "{value}:{spec} {unit}".format(spec=self.defualt_fomat, **self.__dict__)

    def __format__(self, format_spec="5.2f"):
        print("formatting", format_spec)
        if format_spec=="": format_spec=self.defualt_fomat
        return "{value}:{spec} {unit}".format(spec=format_spec, **self.__dict__)

class RTD(object):
    """ 计量以及其他与物理单位相关值的管理。
    速率——时间——距离的计算
    """

    rate = UnitValue("kt")
    time = UnitValue("hr")
    distance = UnitValue("km")

    def __init__(self, rate=None, time=None, distance=None):
        if rate is None:
            self.time = time
            self.distance = distance
            self.rate = distance/time
        if time is None:
            self.rate = rate
            print(self.rate)
            self.distance = distance
            self.time = distance/rate
        if distance is None:
            self.rate = rate
            self.time = time
            self.distance = rate*time


    def __str__(self):
        return "rate:{0.rate} time:{0.time} distance:{0.distance}".format(self)


r = RTD(rate=5.8, distance=12)
print(r)
print(r.time.value, r.time.unit)
print(type(r.time.value))



# 2. 使用数据修饰符
class Unit(object):
    """ 单位修饰符的基类定义
    单位转换：通过简单的乘除运算实现了标准单位和非标准单位的互换。
    """

    conversion = 1.0 # 转换因数

    def __get__(self, instance, owner):
        return instance.kph * self.conversion

    def __set__(self, instance, value):
        instance.kph = value/self.conversion

# 两个转换修饰符类
class Knots(Unit):
    conversion = 0.539968

class MPH(Unit):
    conversion = 0.62137119

class KPH(Unit):
    def __get__(self, instance, owner):
        return instance._kph
    def __set__(self, instance, value):
        instance._kph = value

class Measurement(object):
    kph = KPH()
    knots = Knots()
    mph = MPH()

    def __init__(self, kph=None, mph=None, knots=None):
        if kph: self.kph=kph
        elif mph: self.mph=mph
        elif knots: self.knots=knots
        else: raise TypeError

    def __str__(self):
        return "rate:{0.kph} kph = {0.mph} mph = {0.knots} knots".format(self)

m2 = Measurement(knots=5.9)
print(m2)


