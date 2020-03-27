# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import HuxiuItem
from tutorial.lib.items import replace_withstrip as _

class HuxiuSpider(scrapy.Spider):

    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = [
        "http://www.huxiu.com/index.php"
    ]

    def parse(self, response):
        rpsx = response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]')
        for sel in rpsx:
            item = HuxiuItem()
            item['title'] = _( sel.xpath('h2/a/text()')[0].extract() )
            abslink = sel.xpath('h2/a/@href')[0].extract()
            url = response.urljoin(abslink)
            item['link'] = url
            item['desc'] = _( sel.xpath('div[@class="mob-sub"]/text()')[0].extract() )
            yield item
            # 注册一个回调函数来解析新闻详情
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = HuxiuItem()
        try:
            item['title'] = _( detail.xpath('h1/text()')[0].extract() )
        except:
            item['title'] = _( response.xpath('//div[@class="article-content-title-box"]/div[@class="title"]/text()')[0].extract() )
        item['link'] = response.url
        try:
            item['published'] = _( detail.xpath(
                'div[@class="article-author"]//span[contains(@class, "article-time")]/text()'
            )[0].extract() )
        except:
            item['published'] = ""
        # 以上这条语句相当于以下语句
        # try:
        #     item['published'] = detail.xpath(
        #         'div[@class="article-author"]/div/span[contains(@class, "article-time")]/text()'
        #     )[0].extract()
        # except:
        #     item['published'] = detail.xpath(
        #         'div[@class="article-author"]/span[contains(@class, "article-time")]/text()'
        #     )[0].extract()
        yield item




