## 消息模型

消息通信概念：消费者、生产者、代理
AMQP元素：交换机、队列、绑定
虚拟主机、消息持久换、消息生命周期

1. 点对点
- 每个消息只有一个消费者
- 发送者和接受者没有时间依赖
- 接受者确认消息处理
![posts](static/p2p.jpg)

2. 发布/订阅
- 每个消息有多个订阅者
- 客户端只有订阅后才能收到消息
- 持久订阅和非持久订阅
- 当只有一个订阅者时 ≈ 点对点

![posts](static/pubsub.jpg)

3. 消息应用场景

![posts](static/apply.jpg)

4. 消息投递语义支持
- 最多一次
- 最少一次
- 至少一次

5. RabbitMQ集群架构

![posts](static/clusterstructure.jpg)

6. RabbitMQ逻辑架构

![posts](static/logicalstructure.jpg)

7. RabbitMQ从生产者到消费者的消息流

![posts](static/string.jpg)
