# -*- coding: utf-8 -*-

import json
from  StringIO import StringIO

a = {"a":1, "B": False}

out_s = StringIO()

json.dump(a, out_s)
out_s.flush()

print out_s.getvalue()
in_s = StringIO(out_s.getvalue())
x = json.load(in_s)

print x






# load


# fp = open("json_test.txt", "r")
# x = json.load(fp)
#
# print x


# import shelve
# # 保存数据
# db = shelve.open('student')
#
# db['url1'] = 'Tom'
# db['url2'] = 19
# db['url3'] = [u'篮球', u'看电影', u'弹吉他']
# db['url4'] = {'sno': 1, 'addr': 'xxxx'}
# db['url6'] = [u'篮球', u'看电影', u'弹吉他']
# db['url5'] = {'sno': 1, 'addr': 'xxxx'}
#
#
# # 读取数据
# for key,value in db.items():
#     print(key, ': ', value)