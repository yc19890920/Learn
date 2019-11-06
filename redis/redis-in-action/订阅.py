# -*- coding: utf-8 -*-

import redis, time

#消息订阅
r = redis.StrictRedis(host="192.168.1.24", port=6379, password=None,db=0)
# p = r.pubsub()                         # 开启订阅
# p.subscribe("first-channel")           # 接收订阅的数据,订阅的频道
# while True:
#     message = p.listen()               # 读取接收的数据
#     for item in message:
#         if item["type"] == 'message':  # 判断数据是否是用户发布的数据
#             data = item["data"]        # 取出用户要发布的数据
#             print data
#             print item
#             # {'pattern': None, 'type': 'message', 'channel': 'first-channel', 'data': 'the i is 151'}
#
# # p.unsubscribe("first-channel")		   # 关闭频道



# sub = r.pubsub()
# sub.subscribe('first-channel')
# while True:
#     item = sub.parse_response()
#     # ['message', 'first-channel', 'the i is 106']
#     if item[0] == 'message':
#         data = item[2]        # 取出用户要发布的数据
#         print data
#         print item


p = r.pubsub()
p.subscribe(['test1', 'test2', 'test3'])
p.psubscribe(['foo*', 'bar?', 'foobar+'])
while True:
    message = p.listen()
    for item in message:
        if item['type'] == 'pmessage' or item['type'] == 'message':
            print("item: ",item)
            print("item['channel']: ", item['channel'])
            print("item['data']: ", item['data'])
            p.unsubscribe('test2')
            time.sleep(1)
