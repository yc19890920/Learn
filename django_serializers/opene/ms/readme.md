- [Django DB router for stateful master-slave replication](https://github.com/yandex/django_replicated)

重写了 django_replicated 装饰器方法，其他还是使用默认的即可。 
改写了方法，支持django rest 增加装饰器（支持函数、rest视图），控制主备使用。
```
"""
"""
扩展了 django_replicated 方式，支持django rest 增加装饰器（支持函数、rest视图），控制主备使用。
其他设置还是参考 django_replicated 进行设置即可。
参考链接：  https://github.com/yandex/django_replicated
"""
from django.utils.decorators import method_decorator
from django_replicated.decorators import use_master, use_slave

# 默认不支持有写的操作，一般不会用到整个装饰器，默认就是使用master
use_master = method_decorator(use_master)
# 只有整个函数或视图是涉及到只有查询操作才使用，或者部分走这个装饰器, 
# 假如被装饰的函数或视图包含 transaction.atomic()， 则 此处里面的还是走 master(or default).
use_slave = method_decorator(use_slave)

# 使用： 
@use_master
def func(*args, **kw):
    pass
    
@use_slave
def func(*args, **kw):
    pass
```

settings设置：
```
# setting文件开头引入
from django_replicated.settings import *

DATABASES {
    'default': {
        # ENGINE, HOST, etc.
    },
    'slave': {
        # ENGINE, HOST, etc.
    },
}

# List of slave database aliases. Default database is always master
REPLICATED_DATABASE_SLAVES = ['slave']
# Enable or disable state checking on writes
REPLICATED_CHECK_STATE_ON_WRITE = True
DATABASE_ROUTERS = ['django_replicated.router.ReplicationRouter']
# ------------------------------------
```

假如使用全局的设置，则增加：
```
MIDDLEWARE_CLASSES = [
    ...
    'django_replicated.middleware.ReplicationMiddleware',
    ...
]
```

查看使用是否生效：
```
# 主库
tcpdump -i lo -nnA "host 127.0.0.1 and port 3306"
# 备库
tcpdump -i lo -nnA "host 127.0.0.1 and port 6033"
```




## 数据读写分离，总结以下5种情况需要注意（使用了主从数据库主要注意前面3点， 其他可以在代码中意识到，是不是需要考虑）。
### 1. 边写边读：
边写边读，即先create之后，再filter查询当前记录，然后更新查询的当前记录会报错（NoneType）。 查询时指定 using('default') 不会报错。————因为从数据库还没有更新数据库。
直接使用当前创建的对象更新不会报错，  查询时也不需要指定 using('default')，会直接更新主数据库。 
直接查询当前记录直接update不会报错，  查询时也不需要指定 using('default')，会直接更新主数据库。 
当创建一个对象时，该对象id 作为redis或者其他队列的异步处理时，有可能找不到改对象（查询），需谨慎处理，当然这种数据也可以配置成只从主数据库读取即可。 

```
with transaction.atomic():
    # 创建，master数据库
    tag = Tag.objects.create(name=str(random.randint(1,10000)))
    # 此处 tag.save() 会报错， 查询当前记录使用 slave 数据库, 会报NoneType错误。 ————因为从数据库还没有更新数据库。
    # 处理这种情况时，直接注释下面这行代码，或者指定  using('default')
    # tag = Tag.objects.filter(pk=tag.id).first()
    tag.name = str(random.randint(1,10000))
    tag.save()
    print(tag.name)
```

### 2. 更新关联对象：
```
print("6. 跨数据库更新关系。会报错。查询加了 using('default')不会报错。")  或者 不是以对象的方式更新，而是关联ID
tags = Tag.objects.filter(name__icontains="杨城").using("default")
# tags = Tag.objects.filter(name__icontains="杨城")
with transaction.atomic():
    a = Article.objects.create(
        title="1", content="1"
    )
    a.count = F("count") + 1
    # 此处会报错，关联数据和要修改数据对象不是同一个数据库里面。 ValueError: Cannot assign "<Tag: Tag object (1)>": the current database router prevents this relation.
    # File "/home/python/pyenv/versions/opene/lib/python3.6/site-packages/django/db/models/fields/related_descriptors.py", line 219, in __set__
    # raise ValueError('Cannot assign "%r": the current database router prevents this relation.' % value)
    a.tag = tags[0]
    # a.tag_id = tags[0].id
    a.save()
    for tag in tags:
        tag.count = F("count") - 1
        tag.save()
```

### 3. 比较重要的数据校验，指定 using('default') 进行校验，除非数据库有 主键、唯一、约束 限制。

### 4. 更新数量相关的最好放在一个事物里面，并指定 using('default')，并使用F函数进行更新。
### ———— 经校验可以不指定using('default')， 但是必须请使用 F 函数进行数值更新操作。

### 5. 更新比较频繁的热数据（业务关键读写，客户前端体验要求较高的数据），请不需要使用 备查询，增删改查都使用主数据库。 -- 路由可以办到。
###  -- 可以二次读取从主数据库读取。或者 写之后的马上的读操作访问主库。
###  -- 关键业务读写都由主库承担，非关键业务读写分离。
###  -- 主从同步延迟，数据量比较大的热数据且更新比较频繁， 建议分库分表。 django模型是支持分表的。分库则通过路由指定即可。
###  -- 或者 主主数据库。


### 6. 复杂查询，比如统计类的，可以走备数据库，以下两种情形：———— 读操作多时，可以一主多重， 路由轮询或者随机选择一个从数据库。
```
1. 模型使用 .using("slave")
2. sql语句使用：
cr = connections['slave'].cursor()
cr.execute(sql)
cr.fetchall()
```

### 7. 分表两种方案： （分表：基于字段。 分库：基于业务。）
    1. 动态创建数据库表，并元类方式映射数据模型。（动态创建模型，动态使用模型）
    2. 直接路由写死模型，根据路由规则代理到不同模型




- [Unable to save with save_model using database router](https://stackoverflow.com/questions/26579231/unable-to-save-with-save-model-using-database-router)
- [Django 多数据库联用](https://code.ziqiangxuetang.com/django/django-multi-database.html)
- [【mysql 读写分离】10分钟了解读写分离的作用](https://blog.csdn.net/u013421629/article/details/78793966)
- [谈谈你对Mysql数据库读写分离的了解，并且有哪些注意事项？](https://juejin.im/post/5cbdaf80f265da038d0b444e)
- [MySQL 读写分离](https://blog.csdn.net/justdb/article/details/17331569)
- [数据库读写分离架构，为什么我不喜欢](https://database.51cto.com/art/201801/563213.htm)
- [海量数据分库分表方案（一）算法方案](https://juejin.im/post/5d6b8dbef265da03f47c38df)
- [一次难得的分库分表实践](https://www.lizenghai.com/archives/29036.html)

```
总结
读写分离相对而言是比较简单的，比分表分库简单，但是它只能分担访问的压力，分担不了存储的压力，也就是你的数据库表的数据逐渐增多，
但是面对一张表海量的数据，查询还是很慢的，所以如果业务发展的快数据暴增，到一定时间还是得分库分表。
但是正常情况下，只要当单机真的顶不住压力了才会集群，不要一上来就集群，没这个必要。有关于软件的东西都是越简单越好，复杂都是形势所迫。
一般我们是先优化，优化一些慢查询，优化业务逻辑的调用或者加入缓存等，如果真的优化到没东西优化了然后才上集群，先读写分离，读写分离之后顶不住就再分库分表。
```


```chameleon
三 读写分离提高性能之原因
1.物理服务器增加，负荷增加
2.主从只负责各自的写和读，极大程度的缓解X锁和S锁争用
3.从库可配置myisam引擎，提升查询性能以及节约系统开销
4.从库同步主库的数据和主库直接写还是有区别的，通过主库发送来的binlog恢复数据，
  但是，最重要区别在于主库向从库发送binlog是异步的，从库恢复数据也是异步的
5.读写分离适用与读远大于写的场景，如果只有一台服务器，当select很多时，update和delete会被这些select访问中的数据堵塞，等待select结束，并发性能不高。
  对于写和读比例相近的应用，应该部署双主相互复制
6.可以在从库启动是增加一些参数来提高其读的性能，例如--skip-innodb、--skip-bdb、--low-priority-updates以及--delay-key-write=ALL。
  当然这些设置也是需要根据具体业务需求来定得，不一定能用上
7.分摊读取。假如我们有1主3从，不考虑上述1中提到的从库单方面设置，假设现在1分钟内有10条写入，150条读取。
  那么，1主3从相当于共计40条写入，而读取总数没变，因此平均下来每台服务器承担了10条写入和50条读取（主库不承担读取操作）。
  因此，虽然写入没变，但是读取大大分摊了，提高了系统性能。
  另外，当读取被分摊后，又间接提高了写入的性能。所以，总体性能提高了，说白了就是拿机器和带宽换性能。
  MySQL官方文档中有相关演算公式：官方文档 见6.9FAQ之“MySQL复制能够何时和多大程度提高系统性能”
8.MySQL复制另外一大功能是增加冗余，提高可用性，当一台数据库服务器宕机后能通过调整另外一台从库来以最快的速度恢复服务，因此不能光看性能，也就是说1主1从也是可以的。
```

```
1、what 读写分离 
读写分离，基本的原理是让主数据库处理事务性增、改、删操作（INSERT、UPDATE、DELETE），
而从数据库处理SELECT查询操作。数据库复制被用来把事务性操作导致的变更同步到集群中的从数据库。

2、why 那么为什么要读写分离呢？ 
因为数据库的“写”（写10000条数据到oracle可能要3分钟）操作是比较耗时的。 
但是数据库的“读”（从oracle读10000条数据可能只要5秒钟）。 
所以读写分离，解决的是，数据库的写入，影响了查询的效率。

3、when 什么时候要读写分离？ 
数据库不一定要读写分离，如果程序使用数据库较多时，而更新少，查询多的情况下会考虑使用，利用数据库 主从同步 。
可以减少数据库压力，提高性能。
当然，数据库也有其它优化方案。memcache 或是 表折分，或是搜索引擎。都是解决方法。

4、主从复制与读写分离
在实际的生产环境中，对数据库的读和写都在同一个数据库服务器中，是不能满足实际需求的。
无论是在安全性、高可用性还是高并发等各个方面都是完全不能满足实际需求的。
因此，通过主从复制的方式来同步数据，再通过读写分离来提升数据库的并发负载能力。
有点类似于前面我们学习过的rsync，但是不同的是rsync是对磁盘文件做备份，而mysql主从复制是对数据库中的数据、语句做备份。

4.1、 mysq支持的复制类型

1） 基于语句的复制。在服务器上执行sql语句，在从服务器上执行同样的语句，mysql默认采用基于语句的复制，执行效率高。

2） 基于行的复制。把改变的内容复制过去，而不是把命令在从服务器上执行一遍。

3） 混合类型的复制。默认采用基于语句的复制，一旦发现基于语句无法精确复制时，就会采用基于行的复制。

4.2、 复制的工作过程

1） 在每个事务更新数据完成之前，master在二进制日志记录这些改变。写入二进制日志完成后，master通知存储引擎提交事务。

2） Slave将master的binary log复制到其中继日志。首先slave开始一个工作线程（I/O），I/O线程在master上打开一个普通的连接，然后开始binlog dump process。
binlog dump process从master的二进制日志中读取事件，如果已经跟上master，它会睡眠并等待master产生新的事件，I/O线程将这些事件写入中继日志。

3） Sql slave thread（sql从线程）处理该过程的最后一步，sql线程从中继日志读取事件，并重放其中的事件而更新slave数据，
使其与master中的数据一致，只要该线程与I/O线程保持一致，中继日志通常会位于os缓存中，所以中继日志的开销很小。


5、 mysql读写分离原理
读写分离就是在主服务器上修改，数据会同步到从服务器，从服务器只能提供读取数据，不能写入，实现备份的同时也实现了数据库性能的优化，以及提升了服务器安全。


6、前较为常见的Mysql读写分离分为以下两种：
1）基于程序代码内部实现
    在代码中根据select 、insert进行路由分类，这类方法也是目前生产环境下应用最广泛的。
    优点是性能较好，因为程序在代码中实现，不需要增加额外的硬件开支，缺点是需要开发人员来实现，运维人员无从下手。

2） 基于中间代理层实现
    代理一般介于应用服务器和数据库服务器之间，代理数据库服务器接收到应用服务器的请求后根据判断后转发到，后端数据库，有以下代表性的程序。

（1）mysql_proxy。mysql_proxy是Mysql的一个开源项目，通过其自带的lua脚本进行sql判断。
（2）Atlas。是由 Qihoo 360, Web平台部基础架构团队开发维护的一个基于MySQL协议的数据中间层项目。
    它是在mysql-proxy 0.8.2版本的基础上，对其进行了优化，增加了一些新的功能特性。
    360内部使用Atlas运行的mysql业务，每天承载的读写请求数达几十亿条。支持事物以及存储过程。

（3）Amoeba。由阿里巴巴集团在职员工陈思儒使用序java语言进行开发，阿里巴巴集团将其用户生产环境下，但是他并不支持事物以及存储过程。

经过上述简单的比较，不是所有的应用都能够在基于程序代码中实现读写分离，像一些大型的java应用，如果在程序代码中实现读写分离对代码的改动就较大，
所以，像这种应用一般会考虑使用代理层来实现，那么今天就使用Amoeba为例，完成主从复制和读写分离。

```
























