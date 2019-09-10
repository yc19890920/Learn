- [Tornado Web Server 文档](https://www.osgeo.cn/tornado/)
Tornado是一种 Web 服务器软件的开源版本。
Tornado 和现在的主流 Web 服务器框架（包括大多数 Python 的框架）有着明显的区别：它是非阻塞式服务器，而且速度相当快。
得利于其 非阻塞的方式和对epoll的运用，Tornado 每秒可以处理数以千计的连接，
因此 Tornado 是实时 Web 服务的一个 理想框架。
不过现在与众多的框架比较，Tornado已经被抛在了后面，Django已经超过了它，更不说其他框架了，
只能说Tornado使用纯python开发的性能还是不能与其他框架借助于cython开发的性能相比。



## MYSQL
pip install TorMySQL
- [所有异步mysql实现中性能最高的Mysql](https://github.com/snower/TorMySQL)
所有异步mysql实现中性能最高的,并且工程使用最完善的实现,真正经过高并发大流量考验.
排队削峰
排队超时防止雪崩
链接超时回收
针对异步编程中最容易出现的没有正常关闭链接放入连接池的连接使用调试
特别优化的iostream

## celery
异步MySQL的使用场景还是很有限的，可以尝试使用任务队列来实现，Celery有一个tornado的client
- [mher/tornado-celery · GitHub](https://github.com/mher/tornado-celery)

## redis
pip install tornado-redis
```
redis.connect只调用一次.这是一个阻塞调用,因此应在启动主ioloop之前调用它.所有处理程序之间共享相同的连接对象.

您可以将其添加到您的应用程序设置中

settings = {
    redis = redis_conn
}
app = tornado.web.Application([('/.*', Handler),],
                              **settings)
```

## jwt
- [JWT-Tornado](https://github.com/vsouza/JWT-Tornado) 



## SQLAlchemy


```
1. 为什么要阅读Tornado的源码？
2. 预备知识：我读过的对epoll最好的讲解
3. epoll与select/poll性能，CPU/内存开销对比
4. 开始Tornado的源码分析之旅
5. 鸟瞰Tornado框架的设计模型
6. Tornado源码必须要读的几个核心文件
7. Tornado HTTP服务器的基本流程
8. Tornado RequestHandler和Application类
9. Application对象的接口与起到的作用
10. RequestHandler的分析
11. Tornado的核心web框架tornado.web小结
12. HTTP层：HTTPRequest,HTTPServer与HTTPConnection
13. Tornado在TCP层里的工作机制
14. Tornado TCPServer类的设计解读
15. 从代码分析TCPServer类的机制
16. Tornado高性能的秘密：ioloop对象分析
17. Tornado IOLoop instance()方法的讲解
18. Tornado IOLoop start()里的核心调度
19. Tornado IOLoop与Configurable类
20. 弄清楚HTTPServer与Request处理流程
21. 对socket封装的IOStream机制概览
22. IOStream实现读写的一些细节
23. 番外篇：Tornado的多进程管理分析
```