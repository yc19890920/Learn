# -*- coding: utf-8 -*-
"""
 如果文章获得至少200张支持票，那么网站认为这篇文章是一篇有趣的文章；
 假如这个网站m每天发布1000篇文章，而其中的50篇符合网站对有趣文章的要求，那么网站要做的就是把这50篇文章放到文章列表前100位至少一天；
 另外暂不支持投反对票。

 随着时间流逝而不断减少的评分；
 为了减少内存，规定当一篇文章发布期满一周之后，用户b不能再对其进行投票，评分将固定，投票名单也将被删除。

"""
import time
import uuid

# 文章发布时间 zset
ZSET_ARTICLE_TIME = "article:time:"
# 文章分值 zset
ZSET_ARTICLE_SCORE = "article:score:"

# 文章投票用户名单,set 用户列表
SET_ARTICLE_VOTED = "article:voted:{article_id}"
# 文章散列表， hash
HASH_ARTICLE = "article:{article_id}"
# 文章分组， set
SET_ARTICLE_GROUP = "article:group:{group_id}"
# 文章ID生成器
ID_ARTICLE = "article:id"

ONE_WEEK_IN_SCORES = 7*24*3600
VOTE_SCORE = 432
ARTICLE_PERPAGE = 25

def VoteArticle(redis, user, article):
    """
    文章投票
    需要考虑事务
    """
    cutoff = time.time() - ONE_WEEK_IN_SCORES

    # 判断是否过期投票了
    if redis.zscore(ZSET_ARTICLE_TIME, article) < cutoff:
        return

    article_id = article.partition(":")[-1]
    # 用户投票
    if redis.sadd(SET_ARTICLE_VOTED.format(article_id=article_id), user):
        redis.zincrby(ZSET_ARTICLE_SCORE, VOTE_SCORE, article)
        redis.hincrby(HASH_ARTICLE.format(article_id=article_id), "votes", 1)


def PostArticle(redis, user, title, link, user_uuid=False, article_id=None):
    """
    文章发布
    """
    # 新建一个文章ID
    if article_id is None:
        if user_uuid:
            article_id = str(uuid.uuid1())
        else:
            article_id = str(redis.inreby(ID_ARTICLE))
    voted_key = SET_ARTICLE_VOTED.format(article_id=article_id)
    article_key = HASH_ARTICLE.format(article_id=article_id)
    now = time.time()
    p = redis.pipeline()
    # 将文章发布者加入投票队列，并设置过期时间
    p.sadd(voted_key, user)
    p.expire(voted_key, ONE_WEEK_IN_SCORES)
    # 维护文章数据
    p.hmset(article_key, {
        "title": title,
        "link": link,
        "poster": user,
        "time": now,
        "votes": 1,
    })
    # 维护投票数据
    p.zadd(ZSET_ARTICLE_TIME, {article_key: now})
    p.zadd(ZSET_ARTICLE_SCORE, {article_key: now+VOTE_SCORE})
    p.execute()
    return article_id


def GetArticle(redis, page=1, order=ZSET_ARTICLE_SCORE):
    """
    取出评分最高的文章， 或者
    取出最新发布的文章
    ZREVRANGE 命令 以分值从大到小
    """
    start = (page-1) * ARTICLE_PERPAGE
    end = start + ARTICLE_PERPAGE - 1
    # 按照分值获取多个文章ID
    ids = redis.zrevrange(order, start, end)
    articles = []
    for article_key in ids:
        article_data = redis.hgetall(article_key)
        article_data['id'] = article_key
        articles.append(article_data)
    return articles



def SetArticleGroups(redis, article_id, to_add=None, to_remove=None):
    """
    :param redis:
    :param article_id:
    :param to_add:     加入群组
    :param to_remove:  群组移除文章
    :return:
    """
    to_add = to_add or []
    to_remove = to_remove or []
    article_key = HASH_ARTICLE.format(article_id=article_id)
    p = redis.pipeline()
    for group_id in to_add:
        p.sadd(SET_ARTICLE_GROUP.format(group_id=group_id), article_key)
    for group_id in to_remove:
        p.srem(SET_ARTICLE_GROUP.format(group_id=group_id), article_key)
    p.execute()


def GetGroupsAticle(redis, group_id, page=1, order=ZSET_ARTICLE_SCORE):
    """
    获取群组排名， 文章
    取出某个群组评分最高的文章， 或者
    取出某个群组最新发布的文章
    ZINTERSTORE 对集合和有序集合进行求交集计算得出了新的有序集合。
    :param redis:
    :param group:
    :param page:
    :param order:
    :return:
    """
    # 为每个群组的各种排列顺序都创建一个键
    dest_key = order + str(group_id)
    if not redis.exists(dest_key):
        p = redis.pipeline()
        p.zinterstore(dest_key, [SET_ARTICLE_GROUP.format(group_id=group_id), order])
        p.expire(dest_key, 60)
        p.execute()
    return GetArticle(redis, page=page, order=dest_key)



if __name__ == "__main__":
    import redis
    import random
    redis = redis.Redis(host="192.168.1.24", port=6379, db=0)
    users = [
        {"id": i, "name": u"yc"} for i in range(1, 1000)
        # {"id": 2, "name": u"cc"},
        # {"id": 3, "name": u"dd"},
        # {"id": 4, "name": u"ff"},
    ]
    articles = [
        (1,  u"百度", "https://www.baidu.com/", 1),
        (2,  u"必应", "https://cn.bing.com/", 2),
        (3, u"csdn", "https://www.csdn.net/", 4),
    ]
    groups = [
        {"id": 1, "name": u"中国"},
        {"id": 2, "name": u"美国"},
        {"id": 3, "name": u"国外"},
        {"id": 4, "name": u"搜索"},
    ]
    for article_id, title, link, user_id in articles:
        PostArticle(redis, user_id, title, link, user_uuid=False, article_id=article_id)


    for i in range(1000):
        article = random.choice(articles)
        user = random.choice(users)
        article_key = HASH_ARTICLE.format(article_id=article[0])
        VoteArticle(redis, user["id"], article_key)

    s = GetArticle(redis, page=1, order=ZSET_ARTICLE_SCORE)
    print( s[1]["title"], type(s[1]["title"]) )

    SetArticleGroups(redis, 1, to_add=[1, 4], to_remove=[2,3])
    SetArticleGroups(redis, 2, to_add=[2, 3, 4], to_remove=[1])
    SetArticleGroups(redis, 3, to_add=[1], to_remove=[2, 3, 4])

    print( GetGroupsAticle(redis, 4, page=1, order=ZSET_ARTICLE_SCORE) )
    print( GetGroupsAticle(redis, 1, page=1, order=ZSET_ARTICLE_SCORE) )
    print(GetGroupsAticle(redis, 2, page=1, order=ZSET_ARTICLE_SCORE))
    print(GetGroupsAticle(redis, 3, page=1, order=ZSET_ARTICLE_SCORE))

    lst = redis.keys("article:*")
    redis.delete(*lst)


















