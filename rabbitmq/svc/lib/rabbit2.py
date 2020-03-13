import pika
import time
from queue import Queue, Empty
from pika.exceptions import ConnectionClosed, ChannelClosed
from .logger import get_logger

logger = get_logger(__name__)


class RabbitMQServer:

    def _get_cursor(self, force_new=False):
        if not force_new:
            key = '{}:{}@{}:{}@{}:{}|{}={}'.format(self._user, self._password, self._host, self._port,
                                                   self._exchange_type, self._exchange, self._queue_name,
                                                   self._virtual_host)
            if key in self._cursor_qs:
                cursor_queue = self._cursor_qs[key]
            else:
                cursor_queue = self._cursor_qs[key] = Queue()

            try:
                return cursor_queue.get_nowait()
            except Empty:
                pass

        # start to get a new connection and channel
        logger.debug('Establishing Rabbit MQ Connection; exchange={}, exchange_type={}, queue={}'.
                     format(self._exchange, self._exchange_type, self._queue_name))
        credentials = pika.PlainCredentials(self._user, self._password)
        parameters = pika.ConnectionParameters(host=self._host, port=self._port, virtual_host=self._virtual_host,
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        # declare exchange and exchange type
        channel.exchange_declare(exchange=self._exchange, exchange_type=self._exchange_type, durable=self._durable)

        return connection, channel

    def __init__(self, host, port, user, password, exchange, exchange_type, queue_name, virtual_host, routing_key,
                 durable):
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
        self._cursor_qs = {}
        self._connection, self._channel = self._get_cursor()

    def __del__(self):
        key = '{}:{}@{}:{}@{}:{}|{}={}'.format(self._user, self._password, self._host, self._port, self._exchange_type,
                                               self._exchange, self._queue_name, self._virtual_host)
        self._cursor_qs[key].put_nowait((self._connection, self._channel))

    def update_cursor(self):
        self._connection, self._channel = self._get_cursor(True)


class RabbitPublisher(RabbitMQServer):

    def __init__(self, host, user, password, exchange, exchange_type='fanout', port=5672, queue_name="",
                 virtual_host='my_vhost', routing_key='', durable=True):
        super(RabbitPublisher, self).__init__(host, port, user, password, exchange, exchange_type, queue_name, virtual_host,
                                              routing_key, durable)

    def push(self, message, retries=2):
        # start to publish
        while True:
            try:
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

    def __init__(self, host, user, password, queue_name, callback, exchange='*', exchange_type='fanout', port=5672,
                 virtual_host='my_vhost', routing_key='', durable=True, auto_ack=True):
        super(RabbitConsumer, self).__init__(host, port, user, password, exchange, exchange_type, queue_name,
                                             virtual_host, routing_key, durable)
        self._callback = callback
        self._auto_ack = auto_ack

    def run(self):
        logger.info(' [*] Started and Waiting for queue data...')
        if self._exchange_type == 'topic' and self._routing_key:
            self._channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key=self._routing_key)

        self._channel.basic_consume(queue=self._queue_name, on_message_callback=self._callback, auto_ack=self._auto_ack)
        self._channel.start_consuming()
