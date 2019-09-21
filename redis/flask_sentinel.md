- Python客户端使用安装
pip install redis
复制代码配置在Flask中配置内容如下：
```
# redis 哨兵
REDIS_SENTINELS = [
    ('172.16.33.128', '26379'),
    ('172.16.33.129', '26379'),
    ('172.16.33.130', '26379'),
]
REDIS_SENTINEL_SERVICE_NAME = 'mymaster'

from redis.sentinel import Sentinel
_sentinel = Sentinel(REDIS_SENTINELS)
redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
redis_slave = _sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME)
```

使用示例
```
# 读数据，master读不到数据去slave读
try:
    real_code = redis_master.get(key)
except ConnectionError as e:
    real_code = redis_slave.get(key)

# 写数据，只能在master里写
try:
    current_app.redis_master.delete(key)
except ConnectionError as e:
    logger.error(e)
```