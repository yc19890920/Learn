# -*- coding: utf-8 -*-
import pika
import sys
import time
import settings as c

credentials = pika.PlainCredentials(c.RABBITMQ_USER, c.RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=c.RABBITMQ_HOST, port=c.RABBITMQ_POST, # 主机，端口
        virtual_host=c.RABBITMQ_VHOSTNAME, # 虚拟主机
        credentials=credentials, # 验证
    ))
channel = connection.channel()

#如果生产者先运行并创建了队列这里就可以不用声明，但是有可能消费者先运行 下面的basic_consume就会因为没有队列报错。
#channel.queue_declare(queue="testMQ")
#已经创建的队列，再赋值durable是无法改变的，rabbitmq已经再维护它了。
channel.queue_declare(queue="task_mq", durable=True)

#定义回调函数用于取出队列中的数据
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # time.sleep(5)
    print("ok")
    ch.basic_ack(delivery_tag=method.delivery_tag) #消息持久化

#告诉RabbitMQ在我这个消费者当前消息还没处理完的时候就不要再给我发新消息了。
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    callback,
    queue = "task_mq",
    no_ack = False)

#no-ack ＝ False，如果生产者遇到情况(its channel is closed, connection is closed,
#or TCP connection is lost)挂掉了，那么，RabbitMQ会重新将该任务添加到队列中。
#也就是说如果生产者挂了，消息就没有了!!!

print(" [*] Waiting for messages. To exit press Ctrl + C ")
channel.start_consuming()