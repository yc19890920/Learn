# -*- coding:utf-8 -*-
import pika
from pika import BaseConnection

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# You may ask why we declare the queue again ? we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we‘re not yet sure which program to run first. In such cases it‘s a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(u" 收到： %s" % body.decode("utf8"))

channel.basic_consume(callback, queue='hello', no_ack=True)
print(u'等待。。。')
channel.start_consuming()