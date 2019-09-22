# -*- coding: utf-8 -*-
"""
为了数据不丢失，我们采用了：

    在数据处理结束后发送ack，这样RabbitMQ Server会认为Message Deliver 成功。
    持久化queue，可以防止RabbitMQ Server 重启或者crash引起的数据丢失。
    持久化Message，理由同上。

    但是这样能保证数据100%不丢失吗？

    答案是否定的。问题就在与RabbitMQ需要时间去把这些信息存到磁盘上，这个time window虽然短，但是它的确还是有。
    在这个时间窗口内如果数据没有保存，数据还会丢失。还有另一个原因就是RabbitMQ并不是为每个Message都做fsync：
    它可能仅仅是把它保存到Cache里，还没来得及保存到物理磁盘上。
"""

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

# 确保队列不丢失
channel.queue_declare(queue='task_mq', durable=True)

count = 1
while 1:
    message = "will i come back %d!" % count
    channel.basic_publish(exchange='',
                          routing_key='task_mq',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode = 2, #make messages persistent
                          ))
    print(message)
    count += 1
    time.sleep(0.1)

# message = "will i come back %d!" % count
# channel.basic_publish(exchange='',
#                       routing_key='task_mq',
#                       body=message,
#                       properties=pika.BasicProperties(
#                           delivery_mode = 2, #make messages persistent
#                       ))
print(" [x] Sent 'will i come back!'")
connection.close()