
## 常见的路径名称操作

| 方法 | 描述 | 
| --- | --- | 
| os.path.abspath(path) | 返回绝对路径 | 
| os.path.basename(path) | 返回文件名 | 
| os.path.commonprefix(list) | 返回list(多个路径)中，所有path共有的最长的路径。| 
| os.path.dirname(path) | 返回文件路径| 
| os.path.exists(path)  | 路径存在则返回True,路径损坏返回False| 
| os.path.lexists  | 路径存在则返回True,路径损坏也返回True| 
| os.path.expanduser(path)  | 把path中包含的"~"和"~user"转换成用户目录| 
| os.path.expandvars(path)  | 根据环境变量的值替换path中包含的”$name”和”${name}”| 
| os.path.getatime(path)  | 返回最后一次进入此path的时间。| 
| os.path.getmtime(path)  | 返回在此path下最后一次修改的时间。| 
| os.path.getctime(path)  | 返回path的大小| 
| os.path.getsize(path)  | 返回文件大小，如果文件不存在就返回错误| 
| os.path.isabs(path)  | 判断是否为绝对路径| 
| os.path.isfile(path)  | 判断路径是否为文件| 
| os.path.isdir(path)  | 判断路径是否为目录| 
| os.path.islink(path)  | 判断路径是否为链接| 
| os.path.ismount(path)  | 判断路径是否为挂载点（）| 
| os.path.join(path1[, path2[, ...]])  | 把目录和文件名合成一个路径| 
| os.path.normcase(path)  | 转换path的大小写和斜杠| 
| os.path.normpath(path)  | 规范path字符串形式| 
| os.path.realpath(path)  | 返回path的真实路径| 
| os.path.relpath(path[, start])  | 从start开始计算相对路径| 
| os.path.samefile(path1, path2)  | 判断目录或文件是否相同| 
| os.path.sameopenfile(fp1, fp2)  | 判断fp1和fp2是否指向同一文件| 
| os.path.samestat(stat1, stat2)  | 判断stat tuple stat1和stat2是否指向同一个文件| 
| os.path.split(path)  | 把路径分割成dirname和basename，返回一个元组| 
| os.path.splitdrive(path)   | 一般用在windows下，返回驱动器名和路径组成的元组| 
| os.path.splitext(path)  | 分割路径，返回路径名和文件扩展名的元组| 
| os.path.splitunc(path)  | 把路径分割为加载点与文件| 
| os.path.walk(path, visit, arg)  | 遍历path，进入每个目录都调用visit函数，visit函数必须有 3个参数(arg, dirname, names)，dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数| 
| os.path.supports_unicode_filenames  | 设置是否支持unicode路径名| 

```
# -*- coding: utf-8 -*-

import os


print os.path.abspath(__file__)
# /home/python/git_worker/Test/tests.py

print os.path.realpath(__file__)
# /home/python/git_worker/Test/tests.py

print os.path.basename(__file__)
# tests.py

print os.path.realpath( os.path.dirname(__file__) )
# /home/python/git_worker/Test

print os.path.abspath( os.path.join( os.path.dirname(__file__), '..', 'conf' ) )
# /home/python/git_worker/conf

print os.path.realpath( os.path.join( os.path.dirname(__file__), '../conf' ) )
# /home/python/git_worker/conf
```

## 文档
- [Python os.path模块](https://my.oschina.net/cuffica/blog/33494)
- [python中的os.path.dirname(\__file__)的使用](https://my.oschina.net/joldy/blog/820056)
- [Python中os.path.dirname(\__file__)的用法](http://woodenrobot.me/2016/09/12/Python%E4%B8%ADos-path-dirname-file-%E7%9A%84%E7%94%A8%E6%B3%95/)
- [python os.path模块常用方法详解](http://wangwei007.blog.51cto.com/68019/1104940)