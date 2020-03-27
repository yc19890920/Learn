# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import datetime
# import redis
# import json
# from scrapy import signals, Request
# from scrapy.exporters import JsonItemExporter
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

from tutorial.items import HuxiuItem
from tutorial.model import db_connect, create_news_table, session_scope
from tutorial.model.huxiu_model import HuXiuModel
import logging
log = logging.getLogger(__name__)

class HuxiuPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if isinstance(item, HuxiuItem):
            link = item["link"].encode("utf-8")
            session = self.Session()
            obj = session.query(HuXiuModel).filter(HuXiuModel.link==link).first()
            if obj:
                if "published" in item:
                    obj.published = item["published"].encode("utf-8")
                if "desc" in item:
                    obj.desc = item["desc"].encode("utf-8")
                session.add(obj)
                session.commit()
            else:
                published = item["published"].encode("utf-8") if "published" in item else ""
                desc = item["desc"].encode("utf-8") if "desc" in item else ""
                obj = HuXiuModel(
                    link=link,
                    title=item["title"].encode("utf-8"),
                    desc=desc,
                    published=published,
                )
                session.add(obj)
                session.commit()
                # with session_scope(self.Session) as db:
                #     db.add(obj)
        log.info(item)
        return item

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def close_spider(self, spider):
        pass
