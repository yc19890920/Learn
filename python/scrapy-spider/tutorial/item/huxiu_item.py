# -*- coding: utf-8 -*-

import scrapy

class HuxiuItem(scrapy.Item):
    """虎嗅网新闻Item"""
    title = scrapy.Field()      # 标题
    link = scrapy.Field()       # 链接
    desc = scrapy.Field()       # 简述
    published = scrapy.Field()  # 发布时间

