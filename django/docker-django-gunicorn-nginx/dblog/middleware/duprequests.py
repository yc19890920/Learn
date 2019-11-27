# -*- coding: utf-8 -*-
#
"""
https://github.com/CraveFood/django-duprequests
Middleware for dropping duplicated requests(用于丢弃重复请求的中间件)

另外在settings.py中，你可以设置一些变量：
DUPLICATED_REQUESTS_CACHE_NAME - 缓存的名称（默认值为default）
DUPLICATED_REQUESTS_CACHE_TIMEOUT - 缓存超时（默认值为5;以秒为单位）
DUPLICATED_REQUESTS_COOKIE_NAME - 用户会话中设置的cookie的名称（默认值为dj-request-id）
DUPLICATED_REQUESTS_COOKIE_PREFIX - cookie 前缀，并结合一个随机的UUID来设置响应cookie（默认值是request-id-）
"""

from uuid import uuid4

from django.conf import settings
from django.core.cache import caches
from django.http.response import HttpResponseNotModified

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:   # pragma: nocover
    MiddlewareMixin = object

CACHE_NAME = getattr(settings, 'DUPLICATED_REQUESTS_CACHE_NAME', 'default')
CACHE_TIMEOUT = getattr(settings, 'DUPLICATED_REQUESTS_CACHE_TIMEOUT', 60)
COOKIE_NAME = getattr(settings, 'DUPLICATED_REQUESTS_COOKIE_NAME', 'dj-request-id')
COOKIE_PREFIX = getattr(settings, 'DUPLICATED_REQUESTS_COOKIE_PREFIX', 'request-id-')


class DropDuplicatedRequests(MiddlewareMixin):
    """Middleware that drops requests made in quick succession.
    Uses Django's caching system to check/save each request."""

    def process_request(self, request):
        """
        process_request 先将 cache_key 从 COOKIES 取出， 然后判断 cache_key 是否在缓存里面，有则返回HttpResponseNotModified，无则缓存该cache_key并设置过期时间
        process_response 设置 COOKIE_NAME 为 cache_key。

        --2-- request-id-7a946fcf3c034f0182c8b18c4bf69a9f /core/blog/article/1/ GET
        --3-- request-id-7a946fcf3c034f0182c8b18c4bf69a9f /core/blog/article/1/ GET
        [28/Mar/2018 09:16:06] "GET /core/blog/article/1/ HTTP/1.1" 200 11044
        --1-- request-id-5e81825e84e64c828dcf338358b1e953 /core/blog/article/1/ POST
        ---------view article_modify-------
        --2-- request-id-5e81825e84e64c828dcf338358b1e953 /core/blog/article/1/ POST
        --3-- request-id-5e81825e84e64c828dcf338358b1e953 /core/blog/article/1/ POST
        [28/Mar/2018 09:16:34] "POST /core/blog/article/1/ HTTP/1.1" 302 0
        --2-- request-id-e8467f020d644675be7b2651ac34b003 /core/blog/article GET
        --3-- request-id-e8467f020d644675be7b2651ac34b003 /core/blog/article GET
        """
        # request.visitor = {}
        # request.visitor['country'] = "中国"
        if request.method.lower() not in ('post', 'put', 'delete', 'patch') or request.is_ajax():
            return None

        cache_key = request.COOKIES.get(COOKIE_NAME)
        if not cache_key:
            return None

        cache = caches[CACHE_NAME]
        print('--1--', cache_key, request.path, request.method)
        # print(request.get_host(), request.path_info, request.session, request.user)
        # ['COOKIES', 'DNT', 'FILES', 'GET', 'META', 'POST',
        #  '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
        #  '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
        #  '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
        #  '_encoding', '_get_post', '_get_raw_host', '_get_scheme', '_initialize_handlers', '_load_post_and_files', '_mark_post_parse_error',
        #  '_messages',  '_post_parse_error', '_read_started', '_set_post', '_stream', '_upload_handlers',
        #  'body', 'build_absolute_uri', 'close', 'content_params', 'content_type', 'encoding', 'environ', 'get_full_path', 'get_host',
        #  'get_port', 'get_raw_uri', 'get_signed_cookie', 'is_ajax', 'is_secure', 'method', 'parse_file_upload', 'path', 'path_info',
        #  'read', 'readline', 'readlines', 'resolver_match', 'scheme', 'session', 'upload_handlers', 'user', 'xreadlines']
        if cache_key in cache:
            return HttpResponseNotModified()
        cache.set(cache_key, True, CACHE_TIMEOUT)

    def process_response(self, request, response):
        # if request.method.lower() not in ('post', 'put', 'delete', 'patch') or request.is_ajax():
        #     return response
        # cache_key = request.COOKIES.get(COOKIE_NAME)
        # print('--2--', cache_key, request.path, request.method, request.get_raw_uri())
        # print(request.visitor)
        response.set_cookie(COOKIE_NAME, COOKIE_PREFIX + uuid4().hex)
        # cache_key = request.COOKIES.get(COOKIE_NAME)
        # print('--3--', cache_key, request.path, request.method)
        return response