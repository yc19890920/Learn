"""  https://github.com/koalalorenzo/django-smartcc
https://imququ.com/post/vary-header-in-http.html
Vary头域值指定了一些请求头域，这些请求头域用来决定当缓存中存在一个响应，并且该缓存没有过期失效，
是否被允许去利用此响应去回复后续请求而不需要重验证（revalidation）。
对于一个不能被缓存或失效的响应缓存，Vary头域值用于告诉用户代理选择表现形式（reprentation）的标准。
一个Vary头域值是“*”意味着缓存不能从后续请求的请求头域来决定合适表现形式的响应。

Set some cache-related headers automatically, defining not-authenticated requests as public and authenticated requests as private.
You can also customize these values for specific URLs. This middleware class will also setup these HTTP headers:
    Vary
    Cache-Control
    Expires.
Note: Remember that this middleware requires authentication, so it should be loaded after the django.contrib.auth.middleware.AuthenticationMiddleware!

自动设置一些与缓存相关的标头，将未经身份验证的请求定义为公共的，经过身份验证的请求设为私有的。
您也可以为特定网址自定义这些值。 这个中间件类还将设置这些HTTP标头：
    Vary
    Cache-Control
    Expires.
注意：请记住，此中间件需要身份验证，因此应该在django.contrib.auth.middleware.AuthenticationMiddleware之后加载！


将响应头中的 Cache-Control 字段设为 private，告诉中间实体不要缓存它；
增加 Vary: Accept-Encoding 响应头，明确告知缓存服务器按照 Accept-Encoding 字段的内容，分别缓存不同的版本；
"""
import re
from datetime import datetime, timedelta
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging

# Getting variables from settings
VARY_HEADER = getattr(settings, 'SCC_SET_VARY_HEADER', True)
VARY_HEADERS = getattr(settings, 'SCC_VARY_HEADERS', ['Accept-Encoding', 'Accept-Language', 'Cookie', "User-Agent"])
EXP_HEADER = getattr(settings, 'SCC_SET_EXPIRE_HEADER', True)
MAX_AGE_PUBLIC = getattr(settings, 'SCC_MAX_AGE_PUBLIC', 86400)
MAX_AGE_PRIVATE = getattr(settings, 'SCC_MAX_AGE_PRIVATE', 0)
CACHE_URLS = getattr(settings, 'SCC_CUSTOM_URL_CACHE', [])
DISABLED = getattr(settings, 'SCC_DISABLED', False)

logger = logging.getLogger(__name__)


class SmartCacheControlMiddleware(MiddlewareMixin):
    """
    Set the Cache-Control header automatically, defining not-authenticated
    requests as public (24h of cache by Default) and authenticated requests
    as private ( 0 seconds of cache ). This middleware class will also setup
    these HTTP headers:
        * Vary
        * Cache-Control
        * Expires
    You can customize a specific Cache-control value on each URL. For example
    if we want to avoid cache on /hello/ but always have it on /api/search we
    should write this in our settings file:
    SCC_CUSTOM_URL_CACHE = (
        (r'www\.example\.com/hello/$', 'private', 0),
        (r'www\.example2\.com/api/search$', 'public', 300),
    )
    Other options are available to customize the behaviour of the middleware:
    SCC_VARY_HEADERS: A list of strings specifying which headers to includ in
                      the Vary header.
                      Default value: ['Accept-Encoding', 'Accept-Language', 'Cookie']
    SCC_SET_EXPIRE_HEADER: Define if the middleware should set the Expires
                           header. Default value: True
    SCC_MAX_AGE_PUBLIC: Define the default max-age value in seconds for public
                        requests. Default value: 86400
    SCC_MAX_AGE_PRIVATE: Define the default max-age value in seconds for
                         private requests. Default value: 0

    SCC_DISABLED: Disable the addition of headers, such as during development.
                  Default value: *False*
    """
    def process_response(self, request, response):
        if DISABLED:
            return response

        meta = request.META.get('PATH_INFO', "")
        host = request.META.get('HTTP_HOST', "") + meta
        print(meta, host)

        response['Cache-Control'] = 'public, max-age=%s' % MAX_AGE_PUBLIC
        expire_in = int(MAX_AGE_PUBLIC)

        if VARY_HEADERS:
            response['Vary'] = ', '.join(VARY_HEADERS)

        try:
            if request.user.is_authenticated:
                expire_in = int(MAX_AGE_PRIVATE)
                response['Cache-Control'] = 'private, max-age={}'.format(
                    MAX_AGE_PRIVATE
                )
        except AttributeError:
            logger.warning(
                "smrtcc: Unable to determinate if the user is authenticated"
            )

        for url_pattern, cache_type, max_age, in CACHE_URLS:
            regex = re.compile(url_pattern)

            if regex.match(host):
                expire_in = max_age
                response['Cache-Control'] = '{type}, max-age={age}'.format(
                    type=cache_type,
                    age=max_age
                )

        if EXP_HEADER:
            expires = datetime.utcnow() + timedelta(seconds=expire_in)
            response['Expires'] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return response