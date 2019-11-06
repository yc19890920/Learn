# -*- coding: utf-8 -*-
"""
通过自制的多接收者消息传递操作来代替redis的PUBLISH命令和SUBSCRIBE命令，
即使接收者曾经断开过连接，它也可以一封不漏地所有发给它地消息。

单接收者消息的发送与订阅替代品： lpush, ltrim
多接收者消息的发送与订阅替代品


"""
import uuid
import time
import math
import redis
import json
from redis.exceptions import WatchError

def acquire_lock(redis, lockname, acquire_timeout=10, lock_timeout=30):
    identifire = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    end = time.time() + acquire_timeout
    # 确保传给EXPIRE的都是整数
    lock_timeout = int(math.ceil(lock_timeout))
    while time.time() < end:
        if redis.set(lockname, identifire, ex=lock_timeout, nx=True):  # 以锁名称为键，uuid的值为值，redis服务器setnx保证了只能有一个客户端成功设置键的原子性
            # redis.expire(lockname, lock_timeout)  # 设置键的过期时间，过期自动剔除，释放锁
            return identifire
        elif not redis.ttl(lockname):  # 当锁未被设置过期时间时，重新设置其过期时间
            redis.expire(lockname, lock_timeout)
        time.sleep(0.001)
    return None

def release_lock(redis, lockname, identifier):
    p = redis.pipeline(True)
    lockname = "lock:"+lockname
    while 1:
        try:
            p.watch(lockname)
            if p.get(lockname) == identifier:
                p.multi()
                p.delete(lockname)
                p.execute()
                return True
            p.unwatch()
            break
        except WatchError:
            pass
    return False


####################################################################################
####################################################################################
# 群组id生成
CHAT_GEN_IDS = "chat:ids:"
# 消息ID生成
CHAT_MESSAGE_GEN_IDS = "chat:ids:{chat_id}"
# 群组 有序集合
CHAT_GRUOP = "chat:{chat_id}"
# 用户已看消息 有序集合
CHAT_USER_SEEN = "chat:seen:{user}"
# 消息 有序集合
CHAT_MESSAGE = 'chat:messages:{chat_id}'

def create_chat(redis, sender, recipients, message, chat_id=None):
    """ 创建聊天群组
    :param redis:
    :param sender:     发送者
    :param recipients: 多接收者
    :param message:   消息
    :param chat_id:  群组ID
    :return:
    """
    key_chat_group_ids = CHAT_GEN_IDS
    # 获取新的群组ID
    chat_id = chat_id or (redis.incr(key_chat_group_ids))
    # 创建一个由用户和分值组成的字典，字典里面的信息将被添加到有序集合里面。
    recipients.append(sender)
    recipientsd = {r:0 for r in recipients}

    key_chat_group = CHAT_GRUOP.format(chat_id=chat_id)

    p = redis.pipeline()
    # 将所有参与群聊的用户添加到有序集合里面。
    p.zadd(key_chat_group, recipientsd)
    for r in recipients:
        key_user_seen = CHAT_USER_SEEN.format(user=r)
        # 初始化已读有序集合
        p.zadd(key_user_seen, {chat_id: 0})
    p.execute()
    # 发送消息
    return send_message(redis, chat_id, sender, message)

def send_message(redis, chat_id, sender, message):
    """ 发送消息
    :param redis:
    :param chat_id:
    :param sender:
    :param message:
    :return:
    """
    key_chat_group = CHAT_GRUOP.format(chat_id=chat_id)
    key_chat_message_ids = CHAT_MESSAGE_GEN_IDS.format(chat_id=chat_id)
    key_chat_message = CHAT_MESSAGE.format(chat_id=chat_id)

    identifier = acquire_lock(redis, key_chat_group)
    if not identifier:
        raise Exception("Couldn't get the lock")
    try:
        # 筹备待发送的消息。
        message_id = redis.incr(key_chat_message_ids)
        ts = time.time()
        paked = json.dumps({
            'id': message_id,
            'ts': ts,
            'sender': sender,
            'message': message,
        })
        # 将消息推送至群组
        redis.zadd(key_chat_message, {paked: message_id})
    except:
        pass
    finally:
        release_lock(redis, key_chat_group, identifier)
    return chat_id

def fetch_pending_message(redis, recipient):
    """ 获取消息
    :param redis:
    :param recipient:
    :return:
    """
    key_user_seen = CHAT_USER_SEEN.format(user=recipient)

    # 获取最后接收到的消息ID
    seen = redis.zrange(key_user_seen, 0, -1, withscores=True)
    p = redis.pipeline()
    for chat_id, seen_id in seen:
        key_chat_message = CHAT_MESSAGE.format(chat_id=chat_id)

        p.zrangebyscore(key_chat_message, seen_id+1, 'inf')
    chat_info = zip(seen, p.execute())
    for i, ((chat_id, seen_id), messages) in enumerate(chat_info):
        if not messages:
            continue
        key_chat_group = CHAT_GRUOP.format(chat_id=chat_id)

        messages[:] = map(json.loads, messages)
        # 使用最新收到的消息来更新群组有序集合。
        seen_id = messages[-1]['id']
        redis.zadd(key_chat_group, {recipient: seen_id})
        # 找出那些所有人都已经阅读过的消息
        min_id = redis.zrange(key_chat_group, 0, 0, withscores=True)
        # 更新已读消息有序集合
        p.zadd(key_user_seen, {chat_id: seen_id})
        if min_id:
            key_chat_message = CHAT_MESSAGE.format(chat_id=chat_id)

            # 清除那些已经被所有人阅读过的消息
            p.zremrangebyscore(key_chat_message, 0, min_id[0][1])
        chat_info[i] = (chat_id, messages)
    p.execute()
    return chat_info

def join_chat(redis, chat_id, user):
    """ 加入群组
    :param redis:
    :param chat_id:
    :param user:
    :return:
    """
    key_chat_group = CHAT_GRUOP.format(chat_id=chat_id)
    key_chat_message_ids = CHAT_MESSAGE_GEN_IDS.format(chat_id=chat_id)
    key_user_seen = CHAT_USER_SEEN.format(user=user)

    # 取得最新群组消息ID
    message_id = int(redis.get( key_chat_message_ids ))
    p = redis.pipeline(True)
    # 将用户添加到群组列表里面。
    p.zadd(key_chat_group, { user: message_id })
    # 将群组添加到用户的已读列表里面
    p.zadd(key_user_seen, { chat_id: message_id })
    p.execute()

def leave_chat(redis, chat_id, user):
    """ 离开群组
    :param redis:
    :param chat_id:
    :param user:
    :return:
    """
    key_chat_group = CHAT_GRUOP.format(chat_id=chat_id)
    key_user_seen = CHAT_USER_SEEN.format(user=user)
    key_chat_message_ids = CHAT_MESSAGE_GEN_IDS.format(chat_id=chat_id)
    key_chat_message = CHAT_MESSAGE.format(chat_id=chat_id)

    p = redis.pipeline()
    p.zrem(key_chat_group, user)
    p.zrem(key_user_seen, chat_id)
    # 查找群组剩余成员数量
    p.zcard(key_chat_group)
    if not p.execute()[-1]:
        # 删除群组
        p.delete(key_chat_message)
        p.delete(key_chat_message_ids)
        p.execute()
    else:
        oldest = redis.zrange(key_chat_group, 0, 0, withscores=True)
        # 删除那些已经被所有成员阅读过的消息。
        redis.zremrangebyscore(key_chat_group, 0, oldest[0][1])

if __name__ == "__main__":
    import random
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)

    sender = "Yc"
    recipients = ["Tome", "Lily"]
    message = u'你好'

    chat_id = create_chat(redis, sender, recipients, message, chat_id=None)
    print chat_id

    chat_info = fetch_pending_message(redis, "Tome")
    print chat_info

    sender = "Tome"
    message = u"大家好"
    send_message(redis, chat_id, sender, message)

    join_chat(redis, chat_id, "Xdd")
    chat_info = fetch_pending_message(redis, "Xdd")
    print chat_info

    time.sleep(60)
    leave_chat(redis, chat_id, "Yc")
    leave_chat(redis, chat_id, "Tome")
    leave_chat(redis, chat_id, "Lily")
    leave_chat(redis, chat_id, "Xdd")
