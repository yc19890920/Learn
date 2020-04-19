

```
redis-py提供两个类Redis和StrictRedis用于实现Redis的命令，
StrictRedis用于实现大部分官方的命令，并使用官方的语法和命令（比如，SET命令对应与StrictRedis.set方法）
Redis是StrictRedis的子类，用于向后兼容旧版本的redis-py
```

```
## pipeline
可以在一次请求中执行多个命令，这样避免了多次的往返时延
当一组命令中每条命令都不依赖于之前的执行结果, 可以使用
pipe = r.pipeline()
pipe.set('one', 'first')
pipe.set('two', 'second')
pipe.execute()
pipeline中的操作是原子的，要改变这种方式，可以传入transaction=False
pipe = r.pipeline(transaction=False)



import redis
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0) 
redis = redis.StrictRedis(connection_pool=redis_pool)  # 定义了一个连接池类，该类返回连接池中的一个连接给调用者

r = redis.Redis(host='localhost', port=6379, db=0)
```

# 文档
- [Redis实战](http://redisinaction.com/index.html)
- [第2章 使用Redis构建Web应用](http://redisinaction.com/preview/chapter2.html)
- [第3章 Redis命令](http://redisinaction.com/preview/chapter3.html)
- [REDIS基础笔记](http://www.wklken.me/posts/2013/10/19/redis-base.html)
- [Python—操作redis](http://www.cnblogs.com/melonjiang/p/5342505.html)
- [python之 Redis](http://www.cnblogs.com/Chen-PY/p/5311938.html)
- [使用Python操作Redis](http://debugo.com/python-redis/)
- [用redis实现支持优先级的消息队列](http://www.cnblogs.com/laozhbook/p/redis_queue.html)
- [基于Redis实现延迟队列](http://kaito-kidd.com/2016/12/26/delay-queue-based-on-redis/)

- [订阅与发布¶](https://redisbook.readthedocs.io/en/latest/feature/pubsub.html)
- [发布与订阅（pub/sub）](http://redisdoc.com/topic/pubsub.html)
- [Redis 发布订阅](http://www.runoob.com/redis/redis-pub-sub.html)
- [Redis-pub-sub-python](https://linpingta.github.io/blog/2016/04/04/redis-pub-sub-python/)
- [Redis应用场景](http://blog.csdn.net/hguisu/article/details/8836819)
- [Redis 的 5 个常见使用场景](http://blog.jobbole.com/88383/)