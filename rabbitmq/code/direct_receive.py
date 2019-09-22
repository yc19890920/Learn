# -*- coding: utf-8 -*-
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

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
print queue_name



# severities = sys.argv[1:]
# if not severities:
#     sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
#     sys.exit(1)

severities = ['info']

for severity in severities:
    channel.queue_bind(exchange='direct_logs',queue=queue_name,routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()