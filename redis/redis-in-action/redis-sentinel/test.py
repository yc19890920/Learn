# -*- coding: utf-8 -*-

from redis.sentinel import Sentinel

REDIS_SENTINEL_SERVICE_NAME = 'mymaster'

# 指定sentinel的地址和端口号
sentinel = Sentinel([('192.168.1.24', 26382), ('192.168.1.24', 26383), ('192.168.1.24', 26384), ('192.168.1.24', 26385)], socket_timeout=0.01)
# 测试，获取以下主库和从库的信息

print sentinel.discover_master(REDIS_SENTINEL_SERVICE_NAME)
print sentinel.discover_slaves('mymaster')

##配置读写分离
#写节点
master = sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME, socket_timeout=0.01)
#读节点
slave = sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME, socket_timeout=0.01)

###读写分离测试   key
print master.set('oldboy', '123')
print slave.get('oldboy')

