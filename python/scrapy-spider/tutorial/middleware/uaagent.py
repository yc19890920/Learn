# -*- coding: utf-8 -*-

import random
import logging
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
logger = logging.getLogger(__name__)

class RotateUserAgentMiddleware(UserAgentMiddleware):
    """避免被ban策略之一：使用useragent池。
    使用注意：需在settings.py中进行相应的设置。
    更好的方式是使用：
    pip install scrapy-fake-useragent
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    }
    """
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents):
        super(RotateUserAgentMiddleware, self).__init__()
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        ua = random.choice(self.agents)
        request.headers.setdefault('User-Agent', ua)
        logger.debug('Current UserAgent: ' + ua)