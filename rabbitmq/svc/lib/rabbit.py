import pika
import time
from queue import Queue, Empty
from pika.exceptions import ConnectionClosed, ChannelClosed
from .logger import get_logger

logger = get_logger(__name__)


class RabbitMQServer:
    def __init__(self,
                 host, port, user, password,
                 exchange, exchange_type, queue_name, virtual_host, routing_key,
                 durable=True, productor=True):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._exchange = exchange
        self._exchange_type = exchange_type
        self._queue_name = queue_name
        self._virtual_host = virtual_host
        self._routing_key = routing_key
        self._durable = durable
        self._productor = productor
        self._cursor_qs = {}
        self._connection, self._channel = self._get_cursor()

    def __del__(self):
        key = '{}:{}@{}:{}@{}:{}|{}={}'.format(
            self._user, self._password, self._host, self._port,
            self._exchange_type, self._exchange, self._queue_name, self._virtual_host)
        self._cursor_qs[key].put_nowait((self._connection, self._channel))

    def update_cursor(self):
        self._connection, self._channel = self._get_cursor(True)

    def _get_cursor(self, force_new=False):
        if not force_new:
            key = '{}:{}@{}:{}@{}:{}|{}={}'.format(
                self._user, self._password, self._host, self._port,
                self._exchange_type, self._exchange, self._queue_name, self._virtual_host)
            if key in self._cursor_qs:
                cursor_queue = self._cursor_qs[key]
            else:
                cursor_queue = self._cursor_qs[key] = Queue()

            try:
                return cursor_queue.get_nowait()
            except Empty:
                pass
        # start to get a new connection and channel
        logger.debug('Establishing Rabbit MQ Connection; exchange={}, exchange_type={}, queue={}'.format(
            self._exchange, self._exchange_type, self._queue_name))

        # 新建连接
        credentials = pika.PlainCredentials(username=self._user, password=self._password)
        parameters = pika.ConnectionParameters(host=self._host, port=self._port,
                                               virtual_host=self._virtual_host,
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters=parameters)
        # 创建通道
        # 声明队列以向其发送消息消息
        channel = connection.channel()
        # 创建broker
        # declare exchange and exchange type
        channel.exchange_declare(exchange=self._exchange, exchange_type=self._exchange_type, durable=self._durable)
        # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        # 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
        channel.queue_declare(queue=self._queue_name, durable=self._durable)
        if self._productor:
            # 把队列和中间人绑定
            channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key=self._routing_key)
        # else:
        #     channel.basic_qos(prefetch_count=1)  # 添加不按顺序分配消息的参数
        return connection, channel


class RabbitPublisher(RabbitMQServer):

    def __init__(self,
                 host="127.0.0.1", port=5672, user=None, password=None,
                 exchange="*", exchange_type='fanout', queue_name='',
                 virtual_host='my_vhost', routing_key='', durable=True):
        super(RabbitPublisher, self).__init__(
            host, port, user, password,
            exchange, exchange_type, queue_name,
            virtual_host, routing_key, durable=durable, productor=True)

    def push(self, message, retries=2):
        # start to publish
        while True:
            try:
                # 注意当未定义exchange时，routing_key需和queue的值保持一致
                # 交换机; 队列名,写明将消息发往哪个队列; 消息内容
                # routing_key在使用匿名交换机的时候才需要指定，表示发送到哪个队列,注意当未定义exchange时，routing_key需和queue的值保持一致
                return self._channel.basic_publish(exchange=self._exchange, routing_key=self._routing_key, body=message)
            except Exception as e:
                if isinstance(e, (ConnectionClosed, ChannelClosed)):
                    time.sleep(10)
                    self.update_cursor()
                    retries -= 1
                    if retries > 0:
                        continue

                raise e


class RabbitConsumer(RabbitMQServer):
    def __init__(self,
                 host="127.0.0.1", port=5672, user=None, password=None,
                 exchange="*", exchange_type='fanout', queue_name='',
                 virtual_host='my_vhost', routing_key='', durable=True,
                 callback=None, auto_ack=True):
        super(RabbitConsumer, self).__init__(
            host, port, user, password,
            exchange, exchange_type, queue_name,
            virtual_host, routing_key, durable=durable, productor=False)
        self._callback = callback
        self._auto_ack = auto_ack

    def run(self):
        logger.info(' [*] Started and Waiting for queue data...')
        if self._exchange_type == 'topic' and self._routing_key:
            self._channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key=self._routing_key)

        self._channel.basic_consume(on_message_callback=self._callback, queue=self._queue_name)
        # 开始监听 接受消息
        self._channel.start_consuming()
