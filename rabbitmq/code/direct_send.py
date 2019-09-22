# -*- coding: utf-8 -*-
"""
需要将一个队列绑定到交换机上，要求该消息与一个特定的路由键完全匹配。
这是一个完整的匹配：
如果一个队列绑定到该交换机上要求路由键 “dog”，则只有被标记为“dog”的消息才被转发，不会转发dog.puppy，也不会转发dog.guard，只会转发dog。
"""
import pika
import sys
import time
import config as c

# Connections 连接
credentials = pika.PlainCredentials(c.RABBITMQ_USER, c.RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=c.RABBITMQ_HOST, port=c.RABBITMQ_POST, # 主机，端口
        virtual_host=c.RABBITMQ_VHOSTNAME, # 虚拟主机
        credentials=credentials, # 验证
    ))
# Channel 信道
channel = connection.channel()

# Exchanges 交换机
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
# Queues 队列
severity = sys.argv[1] if len(sys.argv) > 1 else 'info' # 严重程度,级别

count = 606193
while 1:
    message = ' '.join(sys.argv[2:]) or "Hello World %d!" % count
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=severity,
        body=message)
    print(" [x] Sent %r:%r" % (severity, message))
    count += 1
    time.sleep(1)

connection.close()