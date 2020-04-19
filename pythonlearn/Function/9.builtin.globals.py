# coding: utf-8

"""
测试
"""

import time

class Test(object):
    pass

def test():
    pass

a = 1


print globals() # globals 函数返回一个全局变量的字典，包括所有导入的变量。

# {
#     'a': 1,
#     '__builtins__': <module '__builtin__' (built-in)>,
#     '__file__': 'D:/code/git_worker/python_learn/Function/9.builtin.globals.py',
#     '__package__': None,
#     'test': <function test at 0x00000000033B2A58>,
#     'time': <module 'time' (built-in)>,
#     'Test': <class '__main__.Test'>,
#     '__name__': '__main__',
#     '__doc__': '\n\xe6\xb5\x8b\xe8\xaf\x95\n'
# }

globals()['curent_time'] = time.time
print curent_time()
# 1503544096.52

time.sleep(10)
print curent_time()
# 1503544106.52

