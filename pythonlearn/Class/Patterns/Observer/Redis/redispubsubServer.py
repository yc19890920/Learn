# -*- coding: utf-8 -*-

import redis

class RedisPubSubHelper(object):

    def __init__(self):
    	# redis连接对象
        self.__conn = redis.Redis(host='127.0.0.1')

    def publish(self, channel, message):
    	# redis对象的publish方法（发布）
    	# 往指定的频道中发布信息
        self.__conn.publish(channel, message)
        return True

    def subscribe(self, channel):
    	# 返回了一个发布订阅的对象
        pub = self.__conn.pubsub()
        # 订阅到指定的频道上
        pub.subscribe(channel)
        pub.parse_response()
        return pub
