2）python连接redis
sentinel集群（需要安装python
redis客户端，即执行
"pip install redis"）
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
from redis.sentinel import Sentinel

# 连接哨兵服务器(主机名也可以用域名)
sentinel = Sentinel([('192.168.10.202', 26379),
                     ('192.168.10.203', 26379),
                     ('192.168.10.205', 26379)
                     ],
                    socket_timeout=0.5)

# 获取主服务器地址
master = sentinel.discover_master('mymaster')
print(master)
# 输出：('192.168.10.202', 26379)

# 获取从服务器地址
slave = sentinel.discover_slaves('mymaster')
print(slave)
# 输出：[('192.168.10.203', 26379), ('192.168.10.205', 26379), ('172.31.0.5', 26379)]

# 获取主服务器进行写入
master = sentinel.master_for('mymaster', socket_timeout=0.5, password='redis_auth_pass', db=15)
w_ret = master.set('foo', 'bar')
# 输出：True

# # 获取从服务器进行读取（默认是round-roubin）
slave = sentinel.slave_for('mymaster', socket_timeout=0.5, password='redis_auth_pass', db=15)
r_ret = slave.get('foo')
print(r_ret)
# # 输出：bar