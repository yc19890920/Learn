# -*- coding: utf-8 -*-
#

import re

# 1. 找出链接
x = '''<a href="http://www.baidu.com">百度</a><a href="https://www.google.com/">谷歌</a><img href="https://www.test.com/aa.gif" titile=""/>'''
pattern = re.compile('[href|src]{1}="(https?://.*?)"')
res = pattern.findall(x)
print res
# ['http://www.baidu.com', 'https://www.google.com/', 'https://www.test.com/aa.gif']



