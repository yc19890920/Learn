- [docker+redis【性能优化】](https://www.zhihu.com/people/logic_z/activities)
- [Redis 复制、Sentinel的搭建和原理说明](https://www.cnblogs.com/zhoujinyi/p/5570024.html)
- [Redis哨兵模式（sentinel）学习总结及部署记录](https://www.cnblogs.com/nulige/articles/9269479.html)
- [Detect Redis Config File](https://zhuanlan.zhihu.com/p/50101602)
- [Redis 配置详解（一）](http://cs-cjl.com/2019/04_09_redis_configuration_1)
- [Redis 配置详解（二）](http://cs-cjl.com/2019/04_09_redis_configuration_2)
- [基于Docker搭建Redis一主两从三哨兵](https://juejin.im/post/5d26b03de51d454fa33b1960)



- [Docker部署Redis集群----第一节（docker初认识）](https://zhuanlan.zhihu.com/p/59183420)
- [Docker部署Redis集群----第二节（docker安装centos和指令讲解）](https://zhuanlan.zhihu.com/p/59289156)
- [Docker部署Redis集群----第三节（docker-redis集群主从复制【上】实现篇）](https://zhuanlan.zhihu.com/p/59469757)
- [Docker部署Redis集群----第四节（docker-redis集群主从复制【中】理论篇）](https://zhuanlan.zhihu.com/p/59645839)
- [Docker部署Redis集群----第五节（docker-redis集群主从复制【下】实践篇）](https://zhuanlan.zhihu.com/p/59994464)
- [Docker部署Redis集群----第六节（docker-redis-sentinel集群的机制）](https://zhuanlan.zhihu.com/p/60301388)
- [Docker部署Redis集群----第七节（docker-redis-sentinel集群实现篇）](https://zhuanlan.zhihu.com/p/60753321)
- [Docker部署Redis集群----第八节（docker-redis哨兵集群原理篇）](https://zhuanlan.zhihu.com/p/61549727)
- [Docker部署Redis集群----第九节（docker-redis哨兵集群“轮询分流”篇实例一）](https://zhuanlan.zhihu.com/p/61899757)
- [Docker部署Redis集群----第十节（docker-redis哨兵集群“秒杀”篇实例二）](https://zhuanlan.zhihu.com/p/62327929)
- [Docker部署Redis集群----第十一节（docker-redis哨兵集群总结）](https://zhuanlan.zhihu.com/p/62592482)
- [Docker部署Redis集群----第十二节（docker-redis-cluster集群理论篇）](https://zhuanlan.zhihu.com/p/62635170)
- [Docker部署Redis集群----第十三节（docker-Compose介绍）](https://zhuanlan.zhihu.com/p/62636484)


## 获取Redis镜像
下面的命令会拉取最新的官方版本的redis镜像
$ docker pull redis

查看镜像
$ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
redis               latest              bb0ab8a99fe6        7 days ago          95MB
hello-world         latest              fce289e99eb9        6 months ago        1.84kB


## 获取并修改redis配置文件
redis官方提供了一个配置文件样例，通过wget工具下载下来。我用的root用户，就直接下载到/root目录里了。
$ wget http://download.redis.io/redis-stable/redis.conf

复制代码打开下载下来的文件后，可以看到配置有很多。我只是搭建服务进行试验所以只修改必要的几项。如果要运用到线上，那必须所有的配置都按需求进行修改。
其中redis服务器的master和slave角色使用的配置文件还会有些不同，下面分别进行说明。
对于master而言，配置文件修改以下几项

```
# 注释这一行，表示Redis可以接受任意ip的连接
# bind 127.0.0.1 

# 关闭保护模式
protected-mode no 

# 让redis服务后台运行
daemonize yes 

# 设定密码(可选，如果这里开启了密码要求，slave的配置里就要加这个密码. 只是练习配置，就不使用密码认证了)
# requirepass masterpassword 

# 配置日志路径，为了便于排查问题，指定redis的日志文件目录
logfile "/var/log/redis/redis.log"
```

对于slave而言，配置文件修改以下几项：
```
# 注释这一行，表示Redis可以接受任意ip的连接
# bind 127.0.0.1 

# 关闭保护模式
protected-mode no 

# 让redis服务后台运行
daemonize yes 

# 设定密码(可选，如果这里开启了密码要求，slave的配置里就要加这个密码)
requirepass masterpassword 

# 设定主库的密码，用于认证，如果主库开启了requirepass选项这里就必须填相应的密码
masterauth <master-password>

# 设定master的IP和端口号，redis配置文件中的默认端口号是6379
# 低版本的redis这里会是slaveof，意思是一样的，因为slave是比较敏感的词汇，所以在redis后面的版本中不在使用slave的概念，取而代之的是replica
# 将35.236.172.131做为主，其余两台机器做从。ip和端口号按照机器和配置做相应修改。
replicaof 35.236.172.131 6379

# 配置日志路径，为了便于排查问题，指定redis的日志文件目录
logfile "/var/log/redis/redis.log"
```

## 启动容器
分别在主机和从机上按照上面的方法建立好配置文件，检查无误后就可以开始启动容器了。
我们在三台机器上分别将容器别名指定为 
redis-1, redis-2, redis-3，这样便于区分与说明，docker通过 --name参数来指定容器的别名。redis-1是master上容器的别名，redis-2和redis-3是两个slave上的别名。
下面以运行redis-3容器为例说明容器的启动过程。
另外两台机器上的容器redis-1和redis-2操作是相同的，只是要注意master的配置文件和slave不同。不过首先要启动主服务器，也就是redis-1容器。然后再启动redis-2和redis-3。


# 首先以后台模式运行容器
$ docker run -p 6379:6379 --name redis-3 --restart=always -v /docker_data/redis/redis.conf:/etc/redis/redis.conf -v /docker_data/redis/data:/data -d redis redis-server /etc/redis/redis.conf --appendonly yes
$ docker run -it --name redis-3 -v /root/redis.conf:/usr/local/etc/redis/redis.conf -d -p 6379:6379 redis /bin/bash

# 容器成功启动后，会打印一个长串的容器ID
a3952342094dfd5a56838cb6becb5faa7a34f1dbafb7e8c506e9bd7bb1c2951b
# 通过ps命令查看容器的状态，可以看到redis-3已经启动
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
a3952342094d        redis               "docker-entrypoint.s…"   8 minutes ago       Up 8 minutes        0.0.0.0:6379->6379/tcp   redis-3



