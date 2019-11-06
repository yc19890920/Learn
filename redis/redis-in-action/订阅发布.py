# -*- coding: utf-8 -*-
"""
Redis 发布订阅(pub/sub)是一种消息通信方式：发布者(pub)发送消息，订阅者(sub)接收消息。
Redis 客户端可以订阅任意数量的频道。

0.publish
将信息发布到指定的频道

1.subscribe
订阅一个或者多个频道

2.psubscribe
订阅一个或多个符合特定模式的频道

3.unsubscribe
退订一个或多个频道

4.punsubscribe
退订一个或多个特定模式的频道
"""

import redis

#消息推送
import time
r = redis.StrictRedis(host="192.168.1.24", port=6379, password=None,db=0)
# i = 0
# while True:
#     i += 1
#     r.publish("first-channel", "the i is " + str(i))    #  发送到的频道,发布的内容
#     print("the i is " + str(i))
#     time.sleep(0.1)

index = 1

while True:
    time.sleep(.1)
    r.publish('test1', 'hello    %d' % index)
    r.publish('test2', 'world    %d' % index)
    r.publish('foo', 'msg from foo    %d' % index)
    r.publish('foo1', 'msg from foo1    %d' % index)
    r.publish('foo2', 'msg from foo2    %d' % index)
    r.publish('bar', 'msg from bar    %d' % index)
    r.publish('bar2', 'msg from bar2    %d' % index)
    r.publish('bar3', 'msg from bar3    %d' % index)
    r.publish('foobar', 'msg from foobar    %d' % index)
    r.publish('foobar2', 'msg from foobar2    %d' % index)
    r.publish('foobar3', 'msg from foobar3    %d' % index)
    index += 1


