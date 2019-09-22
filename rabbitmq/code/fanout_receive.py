# -*- coding: utf-8 -*-
import pika
import config as c

credentials = pika.PlainCredentials(c.RABBITMQ_USER, c.RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=c.RABBITMQ_HOST, port=c.RABBITMQ_POST, # 主机，端口
        virtual_host=c.RABBITMQ_VHOSTNAME, # 虚拟主机
        credentials=credentials, # 验证
    ))
channel = connection.channel()


channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
result = channel.queue_declare(queue="fanout:queue", exclusive=False)
queue_name = result.method.queue
print queue_name

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback, queue=queue_name,no_ack=True)

channel.start_consuming()