# -*- coding: utf-8 -*-
import time
import pika
import sys
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
channel.queue_declare(queue="fanout:queue", exclusive=False)

count = 1
while count:
    message = ' '.join(sys.argv[1:]) or "info: Hello World %d!" % count
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
    count += 1
    time.sleep(0.1)
connection.close()