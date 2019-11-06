# -*- coding: utf-8 -*-
"""
ActiveMQ / RabbitMQ / Gearman / Amazon SQS
任务队列 先进先出（FIFO）队列  后进先出（LIFO）队列  优先级（priority）队列  延迟队列
"""
import json
import uuid
import time
import redis

#####################################################################################################################
# 任务队列
def send_email_prd(redis, seller, item, price, buyer):
    """ 先到先服务
    lpush  brpop
    :param redis:
    :param seller:
    :param item:
    :param price:
    :param buyer:
    :return:
    """
    data = {
        "seller": seller,
        "item": item,
        "price": price,
        "buyer": buyer,
    }
    redis.lpush('queue:email', json.dumps(data))

def send_mail_process(redis):
    """ 多个看执行任务（同一类型的发邮件需求），
    则传过来的参数格式为[ "FUNCTION_NAME", [arg1, args2,...] ],  然后维护一个 callbacks 字典进行映射方法即可。
    def aa(s): print "aa" + s
    def bb(s):  print "bb" + s
    callbacks = { "aa": aa, "bb": bb }
    callbacks['aa']('xx')
    :param redis:
    :return:
    """
    while 1:
        packed = redis.brpop('queue:email', timeout=30)
        if not packed: continue
        to_send = json.loads(packed[1])
        # 发送流程


#####################################################################################################################
# 优先级队列
def send_mail_process2(redis):
    """ 多个看执行任务（同一类型的发邮件需求），
    则传过来的参数格式为[ "FUNCTION_NAME", [arg1, args2,...] ],  然后维护一个 callbacks 字典进行映射方法即可。
    def aa(s): print "aa" + s
    def bb(s):  print "bb" + s
    callbacks = { "aa": aa, "bb": bb }
    callbacks['aa']('xx')
    :param redis:
    :return:
    """
    while 1:
        # 从高中低依次取数据，直到高，中，低依次没有数据了。
        queues = ['queue:email:high', 'queue:email:middle', 'queue:email:low']
        packed = redis.brpop(queues, timeout=30)
        if not packed: continue
        to_send = json.loads(packed[1])
        # 发送流程


#####################################################################################################################
# 延迟任务队列
def execute_later(redis, queue, name, args, delay=0):
    identifier = str(uuid.uuid4())
    item = json.dumps([identifier, queue, name, args])
    if delay>0:
        redis.zadd('delayed:queue:', { item: time.time()+delay })
    else:
        redis.rpush('queue:'+queue, item)
    return identifier

def poll_queue(redis):
    while 1:
        item = redis.zrange('delayed:queue:', 0, 0, withscores=True)
        # 任务集合没有任务，或者任务的执行时间未到。
        if not item or item[0][1] > time.time():
            time.sleep(0.01)
            continue

        # 解码要被执行的任务，弄清除它应该被推入哪个任务队列。
        item = item[0][0]
        identifier, queue, name, args = json.loads(item)

        # 为了对任务进行移动尝试获取锁
        # 细粒度锁
        locked = acquire_lock(redis, identifier)
        if not locked:
            continue

        # 将任务推入适当的任务队列里面。
        if redis.zrem('delayed:queue:', item):
            redis.lpush('queue:'+queue, item)
        release_lock(redis, identifier, locked)


#####################################################################################################################
# 延迟的优先级任务队列
# ['high-delayed', 'medium-delayed', 'low-delayed']