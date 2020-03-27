# -*- coding: utf-8 -*-

import base64
import logging
from itertools import cycle
from tutorial.settings import PROXIES
logger = logging.getLogger(__name__)

class ProxyMiddleware(object):
    """cover scrapy's HttpProxyMiddleware.
       if 'proxy' in request.meta, HttpProxyMiddleware don't do anything.
     """
    def __init__(self):
        self.proxyes = cycle(PROXIES)

    def process_request(self, request, spider):
        """overwrite method"""
        proxy = next(self.proxyes)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            logging.info('[ProxyMiddleware] proxy:%s is used', proxy['ip_port'])
        else:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            logging.info('[ProxyMiddleware] proxy:%s is used', proxy['ip_port'])

        # if 'proxy' in request.meta:
        #     return
        # proxy = next(self.proxyes)["http"]
        # request.meta['proxy'] = proxy
        # encoded_user_pass = base64.encodestring(proxy['user:pass'])
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        # logging.info('[ProxyMiddleware] proxy:%s is used', proxy)