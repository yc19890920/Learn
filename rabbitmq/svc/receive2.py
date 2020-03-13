import time
import json
from lib.rabbit import RabbitConsumer
# from lib.rabbit2 import RabbitConsumer
from lib.logger import get_logger

logger = get_logger(__name__)

RABBIT_HOST = "192.168.1.24"
RABBIT_PORT = 10000
RABBIT_USER = "yc"
RABBIT_PASSWORD = "123456"

VHOST = "my_vhost"
exchange_type = "direct"  # fanout

ROUTING_KEY = ""
QUEUE = 'direct-quque'  # 队列名
EXCHANGE = 'direct-exchange'  # "fanout-exchange"
if exchange_type == 'direct' and not ROUTING_KEY:
    ROUTING_KEY = "direct-key"


def rabbit_callback(ch, method, properties, body):
    """ 更多Rabbit MQ、回调处理消息内容以及订单数据格式，参考rabbit.rd文件说明 """

    # 由于部分Python版本得到的body数据是bytes，因此需要转换一下
    if isinstance(body, bytes):
        body = body.decode('utf-8')

    logger.info(' [C] Receive body={}'.format(body))
    is_error = False
    try:
        # cover body data to json data
        json_data = json.loads(body)
        if not (json_data and isinstance(json_data, dict)):
            logger.warning('Rabbit MQ message body is not json format, body={}'.format(body))
            return

        # get the message type
        message_type = json_data.get('type', '')
        if message_type != 'orders':
            logger.warning('Rabbit MQ message type is invalid, type={}, body={}'.format(message_type, body))
        # time.sleep(1)
        pass
    except Exception as e:
        logger.error('Deal with rabbit data error, body={} error: {}'.format(body, e))
        is_error = True
    finally:
        if is_error:
            ch.basic_nack(delivery_tag=method.delivery_tag)  # 发送ack消息
            raise
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    r = RabbitConsumer(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        user=RABBIT_USER,
        password=RABBIT_PASSWORD,
        exchange=EXCHANGE,
        exchange_type=exchange_type,
        queue_name=QUEUE,
        routing_key=ROUTING_KEY,
        virtual_host=VHOST,
        callback=rabbit_callback,
        auto_ack=False,
    )
    r.run()
