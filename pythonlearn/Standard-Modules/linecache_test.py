# -*- coding: utf-8 -*-

import linecache

# 读取文件某一行的内容
content = linecache.getline("linecache.md", 5)
print content

lists = linecache.getlines("linecache.md")
print lists

linecache.clearcache()

