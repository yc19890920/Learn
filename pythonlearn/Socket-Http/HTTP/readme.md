

## HTTP
- [HTTP 协议简介](https://www.ctolib.com/docs/sfile/explore-python/HTTP/HTTP.html)
- [http-api-guide](https://github.com/bolasblack/http-api-guide)


## Requests
> - [Requests 库的使用](https://www.ctolib.com/docs/sfile/explore-python/HTTP/Requests.html)
> - [Requests latest](http://docs.python-requests.org/zh_CN/latest/)
>> - [1.Requests 快速上手](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)
>> - [2.Requests 高级用法](http://docs.python-requests.org/zh_CN/latest/user/advanced.html)
>> - [3.Requests 身份认证](http://docs.python-requests.org/zh_CN/latest/user/authentication.html)
>> - [4.Requests 推荐的库和扩展](http://docs.python-requests.org/zh_CN/latest/community/recommended.html)
>> - [5.Requests API 文档/指南](http://docs.python-requests.org/zh_CN/latest/community/recommended.html)

> - [Python HTTP 库：requests 快速入门](https://liam0205.me/2016/02/27/The-requests-library-in-Python/)
> - [Python Requests快速入门](http://blog.csdn.net/xiaoxinyu316/article/details/51089883)



## urllib
- [Python核心模块——urllib模块](http://www.cnblogs.com/sysu-blackbear/p/3629420.html)
- [20.5. urllib — Open arbitrary resources by URL通过URL打开任意资源](http://python.usyiyi.cn/documents/python_278/library/urllib.html)

## urllib2  
- [Python 标准库 urllib2 的使用细节](http://zhuoqiang.me/python-urllib2-usage.html)
- [urllib与urllib2的学习总结(python2.7.X)](http://www.cnblogs.com/wly923/archive/2013/05/07/3057122.html)
- [20.6. urllib2 — 扩展库for opening URLS](http://python.usyiyi.cn/documents/python_278/library/urllib2.html)

### python3
- [urllib](http://python.usyiyi.cn/documents/python_352/library/urllib.html#module-urllib)	
> - [urllib.error] 由urllib.request引发的异常类
> - [urllib.parse]	URL解析组件
> - [urllib.request]	用于打开网址的可扩展库。
> - [urllib.response]	urllib使用的响应类。
> - [urllib.robotparser] 	加载robots.txt文件并回答有关其他网址可抓取性的问题。

## urllib3  ————重点

- Urllib3是一个功能强大，条理清晰，用于HTTP客户端的Python库，许多Python的原生系统已经开始使用urllib3。Urllib3提供了很多python标准库里所没有的重要特性：
> 1、 线程安全
> 2、 连接池 （多次请求中可重复利用同一socket连接）
> 3、 客户端SSL/TLS验证
> 4、 文件分部编码上传 (File posting)
> 5、 协助处理重复请求和HTTP重定位  (内置重定向和重试)
> 6、 支持压缩编码 (支持gzip和deflate解码)
> 7、 支持HTTP和SOCKS代理
> 8、 100%测试覆盖率
> 9、 支持AppEngine、gevent和eventlib
> 10、Requests库使用了urllib3

- [Python--urllib3库详解1](http://www.cnblogs.com/KGoing/p/6146999.html)
- [Urllib3：具有线程安全连接池、文件post等功能的Python HTTP库](http://hao.jobbole.com/urllib3/)
- [urllib3](https://urllib3.readthedocs.io/en/latest/)
> - [User Guide](https://urllib3.readthedocs.io/en/latest/user-guide.html)
> - [Advanced Usage](https://urllib3.readthedocs.io/en/latest/advanced-usage.html)
> - [Reference](https://urllib3.readthedocs.io/en/latest/reference/index.html)




## python中 urllib, urllib2, httplib, httplib2 几个库的区别    ————重点
- [设计符合 Python 编程理念的应用编程接口](http://codingpy.com/article/designing-pythonic-apis/)
- [python中 urllib, urllib2, httplib, httplib2 几个库的区别](https://my.oschina.net/sukai/blog/611451)
- [详解：Python2中的urllib、urllib2与Python3中的urllib以及第三方模块requests](http://www.voidcn.com/article/p-zbjewacj-bmp.html)


## 小结

- **urllib3 提供线程安全连接池和文件post支持,与urllib及urllib2的关系不大. **
- **requests 自称HTTP for Humans, 使用更简洁方便**


### Python2
- Python2: urllib和urllib2的主要区别:
> urllib2可以接受Request对象为URL设置头信息,修改用户代理,设置cookie等, urllib只能接受一个普通的URL.
> urllib提供一些比较原始基础的方法而urllib2没有这些, 比如 urlencode

- httplib 和 httplib2 httplib 是http客户端协议的实现,通常不直接使用, urllib是以httplib为基础 httplib2 是第三方库, 比httplib有更多特性

### Python3

- urllib( python2中的urllib和urllib2合并 )，此包分成了几个模块：
```
urllib.request 用于打开和读取URL, 
urllib.error 用于处理前面request引起的异常, 
urllib.parse 用于解析URL, 
urllib.robotparser用于解析robots.txt文件
```

- python2.X 中的 urllib.urlopen()被废弃, urllib2.urlopen()相当于python3.X中的urllib.request.urlopen()





