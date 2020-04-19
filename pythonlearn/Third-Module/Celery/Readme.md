
## 异步任务神器 Celery

在程序的运行过程中，我们经常会碰到一些耗时耗资源的操作，为了避免它们阻塞主程序的运行，我们经常会采用多线程或异步任务。
比如，在 Web 开发中，对新用户的注册，我们通常会给他发一封激活邮件，而发邮件是个 IO 阻塞式任务，如果直接把它放到应用当中，就需要等邮件发出去之后才能进行下一步操作，此时用户只能等待再等待。
更好的方式是在业务逻辑中触发一个发邮件的异步任务，而主程序可以继续往下运行。

Celery 是一个强大的分布式任务队列，它可以让任务的执行完全脱离主程序，甚至可以被分配到其他主机上运行。
我们通常使用它来实现异步任务（async task）和定时任务（crontab）。它的架构组成如下图：

![Celery.png](https://github.com/yc19890920/python_learn/blob/master/Third-Module/Celery/img/Celery.png)

可以看到，Celery 主要包含以下几个模块：

> - 任务模块 Task

>> 包含异步任务和定时任务。其中，异步任务通常在业务逻辑中被触发并发往任务队列，而定时任务由 Celery Beat 进程周期性地将任务发往任务队列。

> - 消息中间件 Broker

>> Broker，即为任务调度队列，接收任务生产者发来的消息（即任务），将任务存入队列。Celery 本身不提供队列服务，官方推荐使用 RabbitMQ 和 Redis 等。

> - 任务执行单元 Worker

>> Worker 是执行任务的处理单元，它实时监控消息队列，获取队列中调度的任务，并执行它。

> - 任务结果存储 Backend

>> Backend 用于存储任务的执行结果，以供查询。同消息中间件一样，存储也可使用 RabbitMQ, Redis 和 MongoDB 等。

## 异步任务
> 使用 Celery 实现异步任务主要包含三个步骤：
>> 1.创建一个 Celery 实例
>> 2.启动 Celery Worker
>> 3.应用程序调用异步任务

## 文档
- [异步任务神器 Celery](https://funhacks.net/2016/12/13/celery/)
- [supervisor+celery+celerybeat入门指南](https://github.com/importcjj/notes/issues/2)
- [使用Celery](https://zhuanlan.zhihu.com/p/22304455)
- [Celery - 分布式任务队列](http://docs.jinkan.org/docs/celery/)
- [Celery 4.0.2 documentation](http://docs.celeryproject.org/en/latest/index.html)
- [Celery 4.0.2 documentation » User Guide](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#periodic-tasks)
