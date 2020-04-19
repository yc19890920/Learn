# -*- coding:utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))   # 相当于建立一个socket连接
channel = connection.channel()
# 声明queue
channel.queue_declare(queue='hello')

# RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
import time
while True:
    channel.basic_publish(exchange="", routing_key='hello', body=u'你好！')
    time.sleep(1)
print(u" 发送 ‘你好！‘")
connection.close()

