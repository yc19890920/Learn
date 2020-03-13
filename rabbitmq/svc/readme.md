- [python中RabbitMQ的使用](https://blog.csdn.net/xc_zhou/article/details/80851726)
- [使用python的pika库来操作rabbitmq](https://pengpengxp.github.io/archive/before-2018-11-10/2016-12-05-pika-and-rabbitmq.html)
- [利用Python学习RabbitMQ消息队列](https://www.ctolib.com/topics-46046.html)

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

```
rabbitmq基本管理命令：
一步启动Erlang node和Rabbit应用：sudo rabbitmq-server
在后台启动Rabbit node：sudo rabbitmq-server -detached
关闭整个节点（包括应用）：sudo rabbitmqctl stop

add_user <UserName> <Password>
delete_user <UserName>
change_password <UserName> <NewPassword>
list_users
add_vhost <VHostPath>
delete_vhost <VHostPath>
list_vhosts
set_permissions [-p <VHostPath>] <UserName> <Regexp> <Regexp> <Regexp>
clear_permissions [-p <VHostPath>] <UserName>
list_permissions [-p <VHostPath>]
list_user_permissions <UserName>
list_queues [-p <VHostPath>] [<QueueInfoItem> ...]
list_exchanges [-p <VHostPath>] [<ExchangeInfoItem> ...]
list_bindings [-p <VHostPath>]
list_connections [<ConnectionInfoItem> ...]


一、概念：

Connection： 一个TCP的连接。Producer和Consumer都是通过TCP连接到RabbitMQ Server的。程序的起始处就是建立这个TCP连接。

Channels： 虚拟连接。建立在上述的TCP连接中。数据流动都是在Channel中进行的。一般情况是程序起始建立TCP连接，第二步就是建立这个Channel。

二、队列：

首先建立一个Connection，然后建立Channels，在channel上建立队列

建立时指定durable参数为真，队列将持久化；指定exclusive为真，队列为临时队列，关闭consumer后该队列将不再存在，一般情况下建立临时队列并不指定队列名称，rabbitmq将随机起名，通过result.method.queue来获取队列名：

result = channel.queue_declare(exclusive=True)

result.method.queue

区别：durable是队列持久化与否，如果为真，队列将在rabbitmq服务重启后仍存在，如果为假，rabbitmq服务重启前不会消失，与consumer关闭与否无关；

而exclusive是建立临时队列，当consumer关闭后，该队列就会被删除

三、exchange和bind

Exchange中durable参数指定exchange是否持久化，exchange参数指定exchange名称，type指定exchange类型。Exchange类型有direct，fanout和topic。

Bind是将exchange与queue进行关联，exchange参数和queue参数分别指定要进行bind的exchange和queue，routing_key为可选参数。

Exchange的三种模式：

Direct：

任何发送到Direct Exchange的消息都会被转发到routing_key中指定的Queue

1.一般情况可以使用rabbitMQ自带的Exchange：””(该Exchange的名字为空字符串)；

2.这种模式下不需要将Exchange进行任何绑定(bind)操作；

3.消息传递时需要一个“routing_key”，可以简单的理解为要发送到的队列名字；

4.如果vhost中不存在routing_key中指定的队列名，则该消息会被抛弃。

Demo中虽然声明了一个exchange='yanfa'和queue='anheng'的bind，但是在后面发送消息时并没有使用该exchange和bind，而是采用了direct的模式，没有指定exchange，而是指定了routing_key的名称为队列名，消息将发送到指定队列。

如果一个exchange 声明为direct，并且bind中指定了routing_key,那么发送消息时需要同时指明该exchange和routing_key.

Fanout:

任何发送到Fanout Exchange的消息都会被转发到与该Exchange绑定(Binding)的所有Queue上

1.可以理解为路由表的模式

2.这种模式不需要routing_key

3.这种模式需要提前将Exchange与Queue进行绑定，一个Exchange可以绑定多个Queue，一个Queue可以同多个Exchange进行绑定。

4.如果接受到消息的Exchange没有与任何Queue绑定，则消息会被抛弃。

Demo中创建了一个将一个exchange和一个queue进行fanout类型的bind.但是发送信息时没有用到它，如果要用到它，只要在发送消息时指定该exchange的名称即可，该exchange就会将消息发送到所有和它bind的队列中。在fanout模式下，指定的routing_key是无效的 。

Topic：

任何发送到Topic Exchange的消息都会被转发到所有关心routing_key中指定话题的Queue上

1.这种模式较为复杂，简单来说，就是每个队列都有其关心的主题，所有的消息都带有一个“标题”(routing_key)，Exchange会将消息转发到所有关注主题能与routing_key模糊匹配的队列。

2.这种模式需要routing_key，也许要提前绑定Exchange与Queue。

3.在进行绑定时，要提供一个该队列关心的主题，如“#.log.#”表示该队列关心所有涉及log的消息(一个routing_key为”MQ.log.error”的消息会被转发到该队列)。

4.“#”表示0个或若干个关键字，“*”表示一个关键字。如“log.*”能与“log.warn”匹配，无法与“log.warn.timeout”匹配；但是“log.#”能与上述两者匹配。

5.同样，如果Exchange没有发现能够与routing_key匹配的Queue，则会抛弃此消息。

四、任务分发

1.Rabbitmq的任务是循环分发的，如果开启两个consumer，producer发送的信息是轮流发送到两个consume的。

2.在producer端使用cha.basic_publish()来发送消息，其中body参数就是要发送的消息，properties=pika.BasicProperties(delivery_mode = 2,)启用消息持久化，可以防止RabbitMQ Server 重启或者crash引起的数据丢失。

3.在接收端使用cha.basic_consume()无限循环监听，如果设置no-ack参数为真，每次Consumer接到数据后，而不管是否处理完成，RabbitMQ Server会立即把这个Message标记为完成，然后从queue中删除了。为了保证数据不被丢失，RabbitMQ支持消息确认机制，即acknowledgments。为了保证数据能被正确处理而不仅仅是被Consumer收到，那么我们不能采用no-ack。而应该是在处理完数据后发送ack。

在处理数据后发送的ack，就是告诉RabbitMQ数据已经被接收，处理完成，RabbitMQ可以去安全的删除它了。如果Consumer退出了但是没有发送ack，那么RabbitMQ就会把这个Message发送到下一个Consumer。这样就保证了在Consumer异常退出的情况下数据也不会丢失。

这里并没有用到超时机制。RabbitMQ仅仅通过Consumer的连接中断来确认该Message并没有被正确处理。也就是说，RabbitMQ给了Consumer足够长的时间来做数据处理。

Demo的callback方法中ch.basic_ack(delivery_tag = method.delivery_tag)告诉rabbitmq消息已经正确处理。如果没有这条代码，Consumer退出时，Message会重新分发。然后RabbitMQ会占用越来越多的内存，由于RabbitMQ会长时间运行，因此这个“内存泄漏”是致命的。去调试这种错误，可以通过一下命令打印un-acked Messages：

sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged

4.公平分发：设置cha.basic_qos(prefetch_count=1)，这样RabbitMQ就会使得每个Consumer在同一个时间点最多处理一个Message。换句话说，在接收到该Consumer的ack前，他它不会将新的Message分发给它。

五、注意：

生产者和消费者都应该声明建立队列，网上教程上说第二次创建如果参数和第一次不一样，那么该操作虽然成功，但是queue的属性并不会被修改。

可能因为版本问题，在我的测试中如果第二次声明建立的队列属性和第一次不完全相同，将报类似这种错406, "PRECONDITION_FAILED - parameters for queue 'anheng' in vhost '/' not equivalent"

如果是exchange第二次创建属性不同，将报这种错406, "PRECONDITION_FAILED - cannot redeclare exchange 'yanfa' in vhost '/' with different type, durable, internal or autodelete value"

如果第一次声明建立队列也出现这个错误，说明之前存在名字相同的队列且本次声明的某些属性和之前声明不同，可通过命令sudo rabbitmqctl list_queues查看当前有哪些队列。解决方法是声明建立另一名称的队列或删除原有队列，如果原有队列是非持久化的，可通过重启rabbitmq服务删除原有队列，如果原有队列是持久化的，只能删除它所在的vhost,然后再重建vhost,再设置vhost的权限（先确认该vhost中没有其他有用队列）。
```