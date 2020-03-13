import json
import time
from lib.rabbit import RabbitPublisher
# from lib.rabbit2 import RabbitPublisher
from lib.logger import get_logger

logger = get_logger(__name__)

RABBIT_HOST = "192.168.1.24"
RABBIT_PORT = 10000
RABBIT_USER = "yc"
RABBIT_PASSWORD = "123456"

VHOST = "my_vhost"
exchange_type = "direct" # fanout  direct

ROUTING_KEY = ""
QUEUE = 'direct-quque'  # 队列名  fanout-quque   direct-quque
EXCHANGE = 'direct-exchange'  # fanout-exchange  direct-exchange
if exchange_type == 'direct' and not ROUTING_KEY:
    ROUTING_KEY = "direct-key"

if __name__ == '__main__':
    r = RabbitPublisher(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        user=RABBIT_USER,
        password=RABBIT_PASSWORD,
        exchange=EXCHANGE,
        exchange_type=exchange_type,
        queue_name=QUEUE,
        routing_key=ROUTING_KEY,
        virtual_host=VHOST)
    count = 1
    while 1:
        data = json.dumps({"name": "test", "type": "orders", "count": count})
        ret = r.push(data)
        print(data)
        count += 1
        # time.sleep(0.1)
