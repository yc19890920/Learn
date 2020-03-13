import pika

RABBIT_HOST = "192.168.1.24"
RABBIT_PORT = 10000
RABBIT_USER = "yc"
RABBIT_PASSWORD = "123456"

QUEUE = 'oss.url_test'  # 队列名
routing_key = ""
exchange = 'oss_test'
virtual_host = "my_vhost"

# 新建连接
credentials = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, virtual_host=virtual_host, credentials=credentials)
connection = pika.BlockingConnection(parameters=parameters)
# 创建通道
channel = connection.channel()
channel.queue_declare(queue=QUEUE, durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 发送ack消息


# 添加不按顺序分配消息的参数,可有可无
# channel.basic_qos(prefetch_count=1)
# 告诉rabbitmq使用callback来接收信息
channel.basic_consume(on_message_callback=callback, queue=QUEUE, auto_ack=False)  # no_ack来标记是否需要发送ack，默认是False，开启状态

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
