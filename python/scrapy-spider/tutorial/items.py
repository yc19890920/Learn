# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from tutorial.item.huxiu_item import HuxiuItem

__all__ = [
    "TutorialItem",
    "HuxiuItem", # 虎嗅网
]


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

