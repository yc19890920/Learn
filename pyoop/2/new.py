class FloatFail(float):

    def __init__(self, value, unit):
        super().__init__(value)
        self.unit = unit
"""
s = FloatFail(6.5, "knots")
Traceback (most recent call last):
  File "D:/code/git/pyoop/2/new.py", line 7, in <module>
    s = FloatFail(6.5, "knots")
TypeError: float() takes at most 1 argument (2 given)
"""

class FloatUnits(float):

    def __new__(cls, value, unit):
        obj = super().__new__(cls, value)
        obj.unit = unit
        return obj

s = FloatUnits(6.5, "knots")
print(s)
print(s*10)
print(s.__dict__)
print(s.unit)

Useless = type("Useless", (), {})
# 等价于：
# class Useless:pass
u = Useless()
print(u)
print(u.__dict__)
print(dir(u))
u.aa = 1
print(dir(u))


