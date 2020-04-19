# -*- coding: utf-8 -*-

import redispubsubServer

# 创建一个连接redis的对象（使用发布与订阅模式的redis对象）
r = redispubsubServer.RedisPubSubHelper()
# 指定订阅频道
data = r.subscribe('test:001')
# 接收频道中的内容，代码会阻塞到这里，直到收到消息
print(data.parse_response())