
1. RabbitMQ
2. Redis
> Redis Queue 一款轻量级的P分布式异步任务队列，基于Redis作为broker，将任务存到redis里面，然后在后台执行指定的Job。就目前而言有三套成熟的工具celery，huey ，rq 。
> 按照功能和使用复杂度来排序的话也是 celery>huey>rq. 因为rq 简单，容易上手，所以自己做的系统也会使用RQ作为分布式任务调度系统。
3. ZeroMQ
4. ActiveMQ
5. Kafka/Jafka
6. Redis Queue


- [【Python】轻量级分布式任务调度系统-RQ](http://blog.itpub.net/22664653/viewspace-2124609/)

####    

- [Kafka设计解析（一）- Kafka背景及架构介绍](http://www.jasongj.com/2015/03/10/KafkaColumn1/)
- [Kafka设计解析（二）- Kafka High Availability （上）](http://www.jasongj.com/2015/04/24/KafkaColumn2/)
- [Kafka设计解析（三）- Kafka High Availability （下）](http://www.jasongj.com/2015/06/08/KafkaColumn3/)
- [Kafka设计解析（四）- Kafka Consumer设计解析](http://www.jasongj.com/2015/08/09/KafkaColumn4/)
- [Kafka设计解析（五）- Kafka性能测试方法及Benchmark报告](http://www.jasongj.com/2015/12/31/KafkaColumn5_kafka_benchmark/) 　　 　　 