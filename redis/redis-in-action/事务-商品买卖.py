# -*- coding: utf-8 -*-

"""
买家：hash  users:27  name, funds (姓名/资金)
卖家：
商品：set   inventory:27   ItemO,ItemP, ItemQ
商品价格排序

market: zset 将商品ID和卖家ID拼接起来，拼接结果作用成员存储到市场有序集合里面，商品价值作为分值。
ItemA.4  35
ItemB.7  48
ItemQ.2  60

商品查找和分页都很容易实现。
"""
import time
import redis
from redis.exceptions import WatchError

def listItem(redis, itemid, sellerid, price):
    """ 售卖商品
    将商品放到市场上销售，程序需要将被销售的商品添加到记录市场正在销售商品的有序集合里面，
    并且在添加操作执行的过程中，监视卖家的包裹以确保被销售的商品的确存在于卖家的包裹中。
    :param redis:
    :param itemid:
    :param sellerid:
    :param price:
    :return:
    """
    inventory = "test:inventory:%s" % str(sellerid)
    item = "%s.%s" % (str(itemid), str(sellerid))
    end = time.time()+5
    p = redis.pipeline()
    while time.time() < end:
        try:
            # 监视用户包裹发生的变化
            p.watch(inventory)
            # 如果指定的商品不在用户的包裹里面，那么停止对包裹的监视并返回一个空值
            if not p.sismember(inventory, itemid):
                p.unwatch()
                return 3

            # 把销售的商品添加到商品买卖市场里面。
            p.multi()
            p.zadd("test:market:", {
                item: price
            })
            p.srem(inventory, itemid)
            # 如果执行execute方法没有引发WatchError异常，那么说明事务执行成功，并且对包裹键的监视也已经结束。
            p.execute()
            return 1
        except WatchError: # 用户的包裹已经发生了变化，重试。
            pass
    return 2

def purchase_item(redis, buyerid, itemid, sellerid, lprice):
    buyer = "test:users:%s" % str(buyerid)
    seller = "test:users:%s" % str(sellerid)
    item = "%s.%s" % (str(itemid), str(sellerid))
    inventory = "test:inventory:%s" % str(buyerid)
    end = time.time()+5
    p = redis.pipeline()

    while time.time() < end:
        try:
            # 对商品买卖市场以及买家的个人信息进行监视。
            # 监视商品是确保m买家想要购买的商品仍然有售（或者商品被别人）
            p.watch("test:market:", buyer)

            price = p.zscore("test:market:", item)
            funds = int(p.hget(buyer, "funds"))
            # 钱不够
            if funds <0 or price != lprice or price>funds:
                p.unwatch()
                return 3

            # 将买家支付的钱转移给卖家，然后将被购买的商品转交给买家
            p.multi()
            p.hincrby(seller, "funds", int(price))
            p.hincrby(buyer, "funds", -int(price))
            p.sadd(inventory, itemid)
            p.zrem("test:market:", item)
            p.execute()
            return 1
        except WatchError:
            pass
    return 2

if __name__ == "__main__":
    import random
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)
    users = [
        # {"id": i, "name": u"yc{}".format(i), "funds": random.uniform(50, 100)} for i in range(1, 1000)
        {"id": i, "name": u"yc{}".format(i), "funds": random.randint(20, 100)} for i in range(1, 5)
    ]
    p = redis.pipeline()
    for i in range(1, 5):
        p.hmset("test:users:%d" % i, {"id": i, "name": u"yc{}".format(i), "funds": random.randint(10, 100)})
    p.execute()

    for i in range(1, 5):
        print "user%d: "% i, redis.hgetall("test:users:%d" % i)

    items1 = (
        {"id": 1, "name": "ItemA", "price": random.randint(50, 100)},
        {"id": 2, "name": "ItemB", "price": random.randint(50, 100)},
        {"id": 3, "name": "ItemB", "price": random.randint(50, 100)},
        {"id": 4, "name": "ItemC", "price": random.randint(50, 100)},
        {"id": 5, "name": "ItemD", "price": random.randint(50, 100)},
        {"id": 6, "name": "ItemE", "price": random.randint(50, 100)},
    )
    p = redis.pipeline()
    for i in range(1, 5):
        for j in items1:
            inventory = "test:inventory:%s" % str(i)
            p.sadd(inventory, j["id"])
            # item = "%s.%s" % (str(j["id"]), str(i))
            # p.zadd("test:market:", {
            #     item: j["price"]
            # })
    p.execute()

    itemid = 1
    sellerid = 1
    price = items1[0]['price']
    res = listItem(redis, itemid, sellerid, price)
    print res

    # purchase_item(redis, buyerid, itemid, sellerid, lprice)
    buyerid = 2
    sellerid = 1
    lprice = items1[0]['price']
    res = purchase_item(redis, buyerid, itemid, sellerid, lprice)
    print res

    time.sleep(3600)
    lst = redis.keys("test:*")
    redis.delete(*lst)




