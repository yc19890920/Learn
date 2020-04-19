# -*- coding: utf-8 -*-
#

import re
import sys
import time
import string
import traceback

LETTERS_AND_DIGITS = string.ascii_letters + string.digits

# 自定义异常类
class SomeError(Exception):
    pass

# 自定义错误
class MyExceptionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

############################################################
# 安全调用对象
def safe_call(fn, *args, **kwargs):
    try :
        return fn(*args, **kwargs)
    except Exception, e:
        # sys.stderr.write('call "%s" failure\n %s' % (fn.__name__, e.message))
        # sys.stderr.write(traceback.format_exc())
        print >>sys.stderr, 'call "%s" failure\n %s' % (fn.__name__, e.message)
        print >>sys.stderr, traceback.format_exc()
        return None

# 等待调用成功 (有超时时间)
def time_call(fn, *args, **kwargs):
    try_count=3
    while try_count > 0 :
        res = safe_call(fn, *args, **kwargs)
        if res is not None:
            return res
        print >>sys.stderr, 'try call "%s" count: %d' % (fn.__name__, try_count)
        # sys.stderr.write('try call "%s" count: %d' % (fn.__name__, try_count))
        try_count -= 1
        time.sleep(0.5)
    return

# 等待调用成功 (无超时时间)
def wait_call(fn, *args, **kwargs):
    while True :
        res = safe_call(fn, *args, **kwargs)
        if res is not None:
            return res
        time.sleep(0.5)
    return

