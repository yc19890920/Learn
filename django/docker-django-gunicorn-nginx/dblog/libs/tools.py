# -*- coding: utf-8 -*-

from app.core.models import Prefs
from libs.formats import dict_compatibility
from django_redis import get_redis_connection
from bs4 import BeautifulSoup

def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

def getSmtpAccout():
    redis = get_redis_connection()
    key = "dblog:cce7e4f11fc518f7fff230079ab0edc9:email:server:accout"
    vals = redis.hgetall(key)
    host = dict_compatibility(vals, "host", None)
    port = dict_compatibility(vals, "port", None)
    is_ssl = dict_compatibility(vals, "is_ssl", None)
    account = dict_compatibility(vals, "account", None)
    password = dict_compatibility(vals, "password", None)
    if not host or not port:
        host = Prefs.geValue("mail_server")
        port = Prefs.geValue("mail_port")
        is_ssl = Prefs.geValue("mail_ssl")
        account = Prefs.geValue("mail_sender")
        password = Prefs.geValue("mail_passwd")
        p = redis.pipeline()
        p.hset(key, "host", host)
        p.hset(key, "port", port)
        p.hset(key, "is_ssl", is_ssl)
        p.hset(key, "account", account)
        p.hset(key, "password", password)
        p.expire(key, 3600)
        p.execute()
    return host, int(port), int(is_ssl), account, password

def getSystemRcp():
    return Prefs.geValue("mail_recipient")


def clearHtmlTags(html):
    text = BeautifulSoup(html).get_text()
    text = text.replace("\r", "").replace("\n", "").replace("  ", "")
    return text