# -*- coding: utf-8 -*-
"""
1. 构建两个前缀匹配自动补全程序
2. 构建分布式锁提高性能
3. 通过开发计数信号量来控制并发
4. 构建两个不同用途的任务队列
5. 通过消息拉取系统来实现延迟消息传递
6. 学习如何进行文件分发

两种不同类型的自动补全，使用的结构，算法，时间都不一样.
 # 第一个自动补全通过使用联系人列表来记录用户最近联系过的100个人，并尝试尽可能地减少实现自动补全所需地内存。
 # 第二个自动补全则为更大地联系人列表提供了更好地性能和扩展性，但实现这些列表所花费的内存也会g更多一些。
 列表占用的内存时最少的。
 有序集合，分值都为0，则使用键进行排序。
"""

def add_update_contact(redis, user, contact):
    """
    1. 如果指定的联系人已经存在于最近联系人列表里面，那么从列表里面移除他。
    2. 将指定的联系人添加到最近联系人列表的最前面。
    3. 如果在添加操作完成后，最近联系人列表包含的联系人数量超过了100个，那么对列表进行修剪，只保留位于列表签名的100个联系人。
    :param redis:
    :param user:
    :param contact:
    :return:
    """
    lst = 'recent:' + user
    p = redis.pipeline()
    p.lrem(lst, contact)
    p.lpush(lst, contact)
    p.ltrim(lst, 0, 99)
    p.execute()


def fetch_autocomplete_list(redis, user, prefix):
    """
    :param redis:
    :param user:
    :param prefix:
    :return:
    """
    lst = redis.lrange('recent:' + user, 0, -1)
    # 获取列表之后，可以交给客户端实现。
    matches = []
    prefix = prefix.lower()
    for i in lst:
        if i.lower().startswith(prefix):
            matches.append(i)
    return matches




