# -*- coding: utf-8 -*-

import threading
try:
    from synchronize import make_synchronized
except ImportError:

    def make_synchronized(func):
        import threading
        func.__lock__ = threading.Lock()

        def synced_func(*args, **kws):
            with func.__lock__:
                return func(*args, **kws)

        return synced_func

from functools import wraps
def singleton(cls):
    _instance = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return get_instance

@singleton
class MyClass(object):
    instance = None
    count = 0

    def __init__(self):
        self.blog = "xiaorui.cc"

    @make_synchronized
    def go(self):
        self.count += 1
        print self.count

def worker():
    e = MyClass()
    print id(e)
    e.go()

def test():
    e1 = MyClass()
    e2 = MyClass()
    e1.blog = 123
    print e1.blog # 123
    print e2.blog # 123
    print id(e1)
    print id(e2)
    print '------------------'

if __name__ == "__main__":
    test()
    task = []
    for one in range(300000):
        t = threading.Thread(target=worker)
        task.append(t)

    for one in task:
        one.start()

    for one in task:
        one.join()
