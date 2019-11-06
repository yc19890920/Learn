# -*- coding:utf-8 -*-
import traceback
import time
from redis import WatchError
from django_redis import get_redis_connection
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import deprecate_current_app
from json import dumps
from django.db.models import F
from django.http import HttpResponse
from logging import getLogger

from django_redis.client import DefaultClient
from django_redis_sentinel import SentinelClient
from django_redis.cache import RedisCache
from redis.sentinel import Sentinel
from django.conf import settings

from goods.models import Goods

log = getLogger("django.server")

@deprecate_current_app
@never_cache
def init(request):
    if Goods.objects.filter(id=1).exists():
        Goods.objects.filter(id=1).update(num=20)
    else:
        Goods.objects.create(num=20)
    redis = get_redis_connection("db2")
    redis.set("sales", 20)
    return HttpResponse(dumps({'detail': "ok"}), content_type="application/json")

@deprecate_current_app
@never_cache
def index1(request):
    obj = Goods.objects.get(id=1)
    if obj.num > 0:
        obj.num = F("num") -1
        obj.save()
        return HttpResponse(dumps({'detail': u"您抢到了！"}), content_type="application/json")
    else:
        return HttpResponse(dumps({'detail': u"抢完了，您来晚啦！"}), content_type="application/json")

@deprecate_current_app
@never_cache
def index2(request):
    """
    非常简单的测试秒杀
    正常的应该是根据不同用户，不同商品去设计的。

    with sms_redis.pipeline() as pipe:
        while 1:
            try:
                #关注一个key
                pipe.watch('stock_count’)
                count = int(pipe.get('stock_count'))
                if count > 0:  # 有库存
                    # 事务开始
                    pipe.multi()
                    pipe.set('stock_count', count - 1)
                    # 事务结束
                    pipe.execute()
                    # 把命令推送过去
                break
            except Exception:
                traceback.print_exc()
                continue

    :param request:
    :return:
    """
    # sentinel = Sentinel( settings.REDIS_SENTINEL_DATABASES, socket_timeout=0.01, db=1)
    # redis = sentinel.master_for(settings.REDIS_SENTINEL_SERVICE_NAME, socket_timeout=0.01)
    redis = get_redis_connection("db2")
    # p = redis.pipeline()
    is_ok = False
    is_busy = True
    with redis.pipeline() as p:
        while 1:
            try:
                # 监听销售量
                p.watch("sales")
                # 获取销售量
                sales = int(p.get("sales"))
                # num = redis.get("sales-qty")
                print "sales:{},type:{}".format(sales, type(sales))
                if sales>0:
                    print '==========================1'
                    p.multi()
                    p.decr("sales")
                    p.execute()
                    is_ok = True
                    # --------------------------
                    # 写数据库
                    obj = Goods.objects.get(id=1)
                    obj.num = F("num") - 1
                    obj.save()
                    # --------------------------
                    break
                else:
                    print '==========================2'
                    # p.unwatch()
                    is_busy = False
                    break
            except WatchError:
                print '==========================3'
                print traceback.format_exc()
                time.sleep(0.01)
                continue
            except:
                print '==========================4'
                print traceback.format_exc()

    if is_ok:
        return HttpResponse(dumps({'detail': u"您抢到了！"}), content_type="application/json")
    elif is_busy:
        return HttpResponse(dumps({'detail': u"对不起，服务器太繁忙了！"}), content_type="application/json")
    else:
        return HttpResponse(dumps({'detail': u"抢完了，您来晚啦！"}), content_type="application/json")