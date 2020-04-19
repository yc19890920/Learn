# -*- coding:utf-8 -*-
#
"""
https://my.oschina.net/1123581321/blog/208671
"""
import gevent
from gevent import Greenlet

class Delay:
    """延迟对象
    """
    def __init__(self, f, *args, **kw):
        self.f = f
        self.args = args
        self.kw = kw

    def call(self):
        return self.f(*self.args, **self.kw)

class DelayCall(Greenlet):
    """以一个微线程的方式实现一个延时调用
    example:
    def p(x):
        print x
    d = DelayCall(5, p, "xx")
    d.start() # 会执行 d._run
    """
    def __init__(self, seconds, f, *args, **kw):
        Greenlet.__init__(self)
        self.seconds = seconds
        self.delay = Delay(f, *args, **kw)

    def cancel(self):
        """取消延时调用
        """
        self.kill()

    def _run(self):
        gevent.sleep(self.seconds)
        return self.delay.call()

class LoopingCall(Greenlet):

    """以一个微线程的方式实现一个定时调用 example:
    def p(x):
        print x
    lc = LoopingCall(5, p, "xx")
    lc.start() # 会执行 d._run
    # some condition
    lc.cancel()
    """

    def __init__(self, seconds, f, *args, **kw):
        Greenlet.__init__(self)
        self.seconds = seconds
        self.delay = Delay(f, *args, **kw)

    def cancel(self):
        """取消定时调用
        """
        self.kill()

    def _run(self):
        while True:
            gevent.sleep(self.seconds)
            self.delay.call()
            break