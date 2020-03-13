- [python中RabbitMQ的使用](https://blog.csdn.net/xc_zhou/article/details/80851726)
- [使用python的pika库来操作rabbitmq](https://pengpengxp.github.io/archive/before-2018-11-10/2016-12-05-pika-and-rabbitmq.html)

```
## 关键词说明：
Broker：消息队列服务器实体。
Exchange：消息交换机，它指定消息按什么规则，路由到哪个队列。
Queue：消息队列载体，每个消息都会被投入到一个或多个队列。
Binding：绑定，它的作用就是把exchange和queue按照路由规则绑定起来。
Routing Key：路由关键字，exchange根据这个关键字进行消息投递。
vhost：虚拟主机，一个broker里可以开设多个vhost，用作不同用户的权限分离。
producer：消息生产者，就是投递消息的程序。
consumer：消息消费者，就是接受消息的程序。
channel：消息通道，在客户端的每个连接里，可建立多个channel，每个channel代表一个会话任务。


1.2消息队列运行机制：
（1）客户端连接到消息队列服务器，打开一个channel。
（2）客户端声明一个exchange，并设置相关属性。
（3）客户端声明一个queue，并设置相关属性。
（4）客户端使用routing key，在exchange和queue之间建立好绑定关系。
（5）客户端投递消息到exchange。
（6）exchange接收到消息后，就根据消息的key和已经设置的binding，将消息投递到一个或多个队列里。

注：在声明一个队列后，如果将其持久化，则下次不需要进行声明，因为该队列已经在rabbitMQ中了！！！

例如下面的例子中都为首次声明一个队列！！！


1.3exchange类型：
1.Direct交换机
特点：依据key进行投递
例如绑定时设置了routing key为”hello”，那么客户端提交的消息，只有设置了key为”hello”的才会投递到队列。

2.Topic交换机
特点：对key模式匹配后进行投递，符号”#”匹配一个或多个词，符号” * ”匹配一个词
例如”abc.#”匹配”abc.def.ghi”，”abc.*”只匹配”abc.def”。

3.Fanout交换机
特点：不需要key，采取广播模式，一个消息进来时，投递到与该交换机绑定的所有队列

1.4消息确认
当客户端从队列中取出消息之后，可能需要一段时间才能处理完成，如果在这个过程中，客户端出错了，异常退出了，而数据还没有处理完成，那么非常不幸，这段数据就丢失了，因为rabbitmq默认会把此消息标记为已完成，然后从队列中移除，
消息确认是客户端从rabbitmq中取出消息，并处理完成之后，会发送一个ack告诉rabbitmq，消息处理完成，当rabbitmq收到客户端的获取消息请求之后，或标记为处理中，当再次收到ack之后，才会标记为已完成，然后从队列中删除。当rabbitmq检测到客户端和自己断开链接之后，还没收到ack，则会重新将消息放回消息队列，交给下一个客户端处理，保证消息不丢失，也就是说，RabbitMQ给了客户端足够长的时间来做数据处理。

在客户端使用no_ack来标记是否需要发送ack，默认是False，开启状态
```