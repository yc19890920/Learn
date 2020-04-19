


Python的标准库中的os模块包含普遍的操作系统功能。
这个模块的作用主要是提供与平台无关的功能。
也就是说os模块能够处理平台间的差异问题，使得编写好的程序无需做任何改动就能在另外的平台上运行。
当然，这个模块只是提供了一个轻便的方法使用要依赖操作系统的功能。
有些特定的功能还得使用特定的模块，比如：
如何只是想读或写文件，请使用open()；
如果想操作文件路径，请使用os.path模块；
如果想在命令行中，读入所有文件的所有行，请使用fileinput模块；
使用tempfile模块创建临时文件和文件夹；
更高级的文件和文件夹处理，请使用shutil模块。
如果想要了解os模块的所有内容，可以使用dir(os)方法查看。

## 文档 os
- [Python OS 文件/目录方法](http://www.runoob.com/python/os-file-methods.html)
- [Python os模块参考手册](http://kuanghy.github.io/2015/08/02/python-os)  重点

- [os 模块](http://wiki.jikexueyuan.com/project/explore-python/File-Directory/os.html)


## os.path ( 常见的路径名称操作 )
- [Python os.path模块](https://my.oschina.net/cuffica/blog/33494)
- [python中的os.path.dirname(\__file__)的使用](https://my.oschina.net/joldy/blog/820056)
- [Python中os.path.dirname(\__file__)的用法](http://woodenrobot.me/2016/09/12/Python%E4%B8%ADos-path-dirname-file-%E7%9A%84%E7%94%A8%E6%B3%95/)
- [python os.path模块常用方法详解](http://wangwei007.blog.51cto.com/68019/1104940)


## shutil  ( 高级文件操作 )
- [python(6)-shutil模块](https://www.bbsmax.com/A/RnJWmo3Odq/)
- [shutil模块](http://xukaizijian.blog.163.com/blog/static/170433119201111414053801/)
- [Python默认模块 os和shutil 实用函数](http://www.cnblogs.com/funsion/p/4017989.html)


## stat
- [python stat模块](http://xukaizijian.blog.163.com/blog/static/1704331192011116104440203/)
- [python stat模块](https://my.oschina.net/colben/blog/361458)
