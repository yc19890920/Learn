# -*- coding: utf-8 -*-
"""
高流量的站点通常需要将Django部署在负载平衡proxy之后。
这种方式将带来一些复杂性，其一就是每个request中的远程IP地址(request.META["REMOTE_IP"])将指向该负载平衡proxy，而不是发起这个request的实际IP。
负载平衡proxy处理这个问题的方法在特殊的 X-Forwarded-For 中设置实际发起请求的IP。
因此，需要一个小小的中间件来确保运行在proxy之后的站点也能够在 request.META["REMOTE_ADDR"] 中得到正确的IP地址

如果站点并不位于自动设置 HTTP_X_FORWARDED_FOR 的反向代理之后，请不要使用这个中间件。
 否则，因为任何人都能够伪造 HTTP_X_FORWARDED_FOR 值，而 REMOTE_ADDR 又是依据 HTTP_X_FORWARDED_FOR 来设置，这就意味着任何人都能够伪造IP地址。
只有当能够绝对信任 HTTP_X_FORWARDED_FOR 值得时候才能够使用这个中间件。
"""

from django.utils.deprecation import MiddlewareMixin

class XForwardedForMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()