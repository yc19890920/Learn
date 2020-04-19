# -*- coding:utf-8 -*-

# import redis
# import json
#
#
# import redis
# # redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# # redis = redis.StrictRedis(connection_pool=redis_pool)  # 定义了一个连接池类，该类返回连接池中的一个连接给调用者
#
# redis = redis.Redis(host='localhost', port=6379, db=0)
# # redis.rpush("aa-20171010-1", json.dumps(
# #     [1,2,3, u"邮件"]
# # ))
#
#
# for res in reversed(redis.lrange("aa-20171010-1", 0, -1)):
#     print json.loads(res)


check_addrs = "fdsg54ge11818@qq.com;fdsg54ge11819@qq.com;fdsg54ge11820@qq.com;fdsg54ge11821@qq.com;fdsg54ge11822@qq.com;fdsg54ge11823@qq.com;fdsg54ge11824@qq.com;fdsg54ge11825@qq.com;fdsg54ge11826@qq.com;fdsg54ge11827@qq.com;fdsg54ge11828@qq.com;fdsg54ge11829@qq.com;fdsg54ge11830@qq.com;fdsg54ge11831@qq.com;fdsg54ge11832@qq.com;fdsg54ge11833@qq.com;fdsg54ge11834@qq.com;fdsg54ge11835@qq.com;fdsg54ge11836@qq.com;fdsg54ge11837@qq.com;"

print check_addrs.split(";")