# -*- coding:utf-8 -*-
#
import pika

# 创建简单的连接凭证
credentials = pika.PlainCredentials("test", "test")
# 连接参数
host = "localhost"
host = "192.168.181.130"
port = 5672
conn_params = pika.ConnectionParameters(host=host, port=port, credentials=credentials) # 没有指定virtual_host，使用默认的'/'
# 建立一个实例
# 1. 建立到代理服务器的连接
conn_broker = pika.BlockingConnection(conn_params)

# 2. 声明一个管道，在管道里发消息 # 获得信道
channel = conn_broker.channel()

# 3. 声明交换器
# 通过键""
exchange = "hello-exchange"
channel.exchange_declare(exchange=exchange,
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)

# 4. 声明队列
# 4. 在管道里声明queue, 这一步没有 queuename 将和 routing_key 名称一样
queue_name = "hello-queue"
routing_key = "hola-key"
channel.queue_declare(queue=queue_name)
# 通过键"hola-key"将队列和交换器绑定起来
channel.queue_bind(queue=queue_name,
                   exchange=exchange,
                   routing_key=routing_key)


# 5. 用于处理传入的消息函数
def msg_consumer(channel, method, header, body): # 四个参数为标准格式
    print channel, method, header # 打印是什么
    # print " [x] Received %r" % body
    print body, type(body)
    channel.basic_ack(delivery_tag = method.delivery_tag) # 消息确认 # 告诉生成者，消息处理完成
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer") # 停止消息并退出
        channel.stop_consuming()
    else:
        print body
    return


# 6. 订阅消费者
channel.basic_consume(msg_consumer, # 如果收到消息，就调用callback函数来处理消息
                      queue=queue_name, # 你要从那个队列里收消息
                      consumer_tag="hello-consumer",
                      # no_ack=True  # 写的话，如果接收消息，机器宕机消息就丢了, 一般不写。宕机则生产者检测到发给其他消费者
                      )

# 7. 开始消费
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()  # 开始消费消息