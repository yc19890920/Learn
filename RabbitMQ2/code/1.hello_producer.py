# -*- coding:utf-8 -*-
#
import pika
from pika import spec

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

##################################################
msg_ids = []
# 发送方确认模式处理器
# def confirm_handler(frame):
#     if type(frame.method) == spec.Confirm.SelectOk:
#         print "Channel in 'confirm' mode."
#     elif type(frame.method) == spec.Basic.Nack:
#         if frame.method.delivery_tag in msg_ids:
#                 print 'Message lost!'
#     elif type(frame.method) == spec.Basic.Ack:
#         if frame.method.delivery_tag in msg_ids:
#             print 'Confirm received'
#             msg_ids.remove(frame.method.delivery_tag)
#
# channel.confirm_delivery(callback=confirm_handler)
##################################################

# 3. 声明交换器
exchange = "hello-exchange"
channel.exchange_declare(exchange=exchange,
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)

# 4. 在管道里声明queue, 这一步没有 queuename 将和 routing_key 名称一样
queue_name = "hello-queue"
routing_key = "hola-key"
channel.queue_declare(queue=queue_name)
# 通过键"hola-key"将队列和交换器绑定起来
channel.queue_bind(queue=queue_name,
                   exchange=exchange,
                   routing_key=routing_key)

# 5. 创建文本消息
# msg =sys.argv[1]
msg = u"hello world 杨城"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

channel.basic_qos(prefetch_count=1)  # 类似权重，按能力分发，如果有一个消息，就不在给你发

# 6. 发布消息
import time
while True:
    time.sleep(1)
    channel.basic_publish(body=msg,
                          exchange=exchange,
                          properties=msg_props,
                          routing_key=routing_key)
    # msg_ids.append(len(msg_ids) + 1) #/(hwppc.5) Add ID to tracking list

channel.close()

