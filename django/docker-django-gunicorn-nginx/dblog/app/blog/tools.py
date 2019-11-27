# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django_redis import get_redis_connection
from app.blog.models import Tag, Category, Article, BlogComment, Suggest

REDIS_KEY = "cce7e4f11fc518f7fff230079ab0edc9"

# 标签缓存
def getTaglist():
    redis = get_redis_connection()
    key = "dblog:{}:tag".format(REDIS_KEY)
    field = "tag"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = Tag.objects.all().order_by("name")
        if lists.exists():
            for d in lists.iterator():
                vals.append( { "id": d.id, "name": d.name } )
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 60*60)
            p.execute()
    return vals


# 最热文章列表
def getHotlist():
    redis = get_redis_connection()
    key = "dblog:{}:article:hot".format(REDIS_KEY)
    field = "hot"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = Article.objects.filter(status='p').order_by("-views", '-id')[:10]
        if lists.exists():
            for d in lists.iterator():
                vals.append( { "id": d.id, "title": d.title } )
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 15*60)
            p.execute()
    return vals


# 最新文章列表
def getNewArticlelist():
    redis = get_redis_connection()
    key = "dblog:{}:article:new".format(REDIS_KEY)
    field = "new"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = Article.objects.filter(status='p').order_by('-id')[:10]
        if lists.exists():
            for d in lists.iterator():
                vals.append( { "id": d.id, "title": d.title } )
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 15*60)
            p.execute()
    return vals


# 最新评论
def getNewCommontlist():
    redis = get_redis_connection()
    key = "dblog:{}:comment:new".format(REDIS_KEY)
    field = "new"
    if redis.exists(key):
        vals = json.loads( redis.hget(key, field) )
    else:
        vals = []
        lists = BlogComment.objects.all().order_by('-id')[:10]
        if lists.exists():
            for d in lists.iterator():
                vals.append( { "id": d.id, "article_id": d.article_id, "content": d.content } )
            p = redis.pipeline()
            p.hset(key, field, json.dumps(vals))
            p.expire(key, 15*60)
            p.execute()
    return vals


# 文章点击 缓存
def shouldIncrViews(ip, article_id):
    redis = get_redis_connection()
    key = "dblog:{}:{}:{}:article:view".format(REDIS_KEY, ip, article_id)
    if redis.exists(key):
        return False
    p = redis.pipeline()
    p.set(key, "1")
    p.expire(key, 5*60)
    p.execute()
    return True


def getLinks(ip, article_id):
    redis = get_redis_connection()
    key = "dblog:{}:{}:{}:article:links".format(REDIS_KEY, ip, article_id)
    if redis.exists(key):
        return False
    return True


