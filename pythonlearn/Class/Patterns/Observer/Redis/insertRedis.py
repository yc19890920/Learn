# -*- coding: utf-8 -*-

import redispubsubServer

# 创建一个连接redis的对象（使用发布与订阅模式的redis对象）
r = redispubsubServer.RedisPubSubHelper()
# 向指定的频道发布消息
r.publish('test:001', '123')