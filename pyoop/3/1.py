# 泛型类

class Generic(object):
    pass

g = Generic()

g.attr = "value"
print(g.attr)

# g.unset



# SimpleNamespace类
import types

n = types.SimpleNamespace()

n.attr = "value"
print(n.attr)