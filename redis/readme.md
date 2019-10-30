redis 队列对访问流量进行分流
redis 限流系统的设计

- [Redis 复制、Sentinel的搭建和原理说明](https://www.cnblogs.com/zhoujinyi/p/5570024.html)
- [Redis哨兵模式（sentinel）学习总结及部署记录](https://www.cnblogs.com/nulige/articles/9269479.html)
- [Detect Redis Config File](https://zhuanlan.zhihu.com/p/50101602)
- [Redis 配置详解（一）](http://cs-cjl.com/2019/04_09_redis_configuration_1)
- [Redis 配置详解（二）](http://cs-cjl.com/2019/04_09_redis_configuration_2)



## 获取并修改redis配置文件
redis官方提供了一个配置文件样例，通过wget工具下载下来。我用的root用户，就直接下载到/root目录里了。
$ wget http://download.redis.io/redis-stable/redis.conf

## 获取并修改sentinel配置文件
wget http://download.redis.io/redis-stable/sentinel.conf


- python连接redis集群
redis使用sentinel模式后，原来的python连接redis方案由于主从服务器可能发生切换变得不可用了。
```
import redis
r2 = redis.StrictRedis() # 如果该实例死机将变得不可用
```

使用Sentinel对象
```
import redis
from redis.sentinel import Sentinel
# 创建一个连接对象,连接所有的哨兵，其会自动发现redis实例
sentinel = Sentinel([('192.168.1.20', 26379), ('192.168.1.20', 26379),('192.168.1.20', 26379)], socket_timeout=0.5)

# 获取主服务器进行写入
master = sentinel.master_for('mymaster', socket_timeout=0.5, db=1)
w_ret = master.set('foo', 'bar')

# 获取从服务器进行读取
slave = sentinel.slave_for('mymaster', socket_timeout=0.5, db=1)
r_ret = slave.get('foo')

# master和slave的用法和前面的redis对象一样了，不过slave只能读不能写
```