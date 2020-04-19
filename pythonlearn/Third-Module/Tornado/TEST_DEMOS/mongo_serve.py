# -*- coding: utf-8 -*-
#

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options

import time
import pymongo
from bson import json_util

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

MGO_CFG = {
    'host': "127.0.0.1",
    'port': 27017,
    'username': "mm-mc",
    'dbname': "mm-mc",
    'password': "PFBgatL4Vq63sEP",
}
define("mongo_cfg", default=MGO_CFG, type=dict)

'''
{ "_id" : ObjectId("59f023a9267a8a81ef2ec397"), "addr" : "18932418429@qq.com", "created" : 1508390780, "aaa" : "789" }
{ "_id" : ObjectId("59f023b3267a8a81ef2ec398"), "addr" : "1@qq.com", "created" : 1508390783, "aaa" : "789" }
{ "_id" : ObjectId("59f17c95dabec155be45d6ee"), "addr" : "1@foxmail.com", "created" : 1508390780 }
{ "_id" : ObjectId("59f1abbae357e857d9e55c21"), "addr" : "2@qq.com", "created" : 1508390783 }
{ "_id" : ObjectId("59f1b049e357e857d9e55c22"), "addr" : "5@qq.com", "created" : 1509064860 }
'''

class QQHandler(tornado.web.RequestHandler):

    def get(self):
        addr = self.get_argument("addr", "")
        print '-----------', addr
        coll = self.application.db.invalidqq
        word_doc = coll.find_one({"addr": addr})
        if word_doc:
            res = json_util.dumps(word_doc)
            self.write(res)
            # del word_doc["_id"]
            # self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})

    def post(self):
        addr = self.get_argument("addr")
        coll = self.application.db.invalidqq
        word_doc = coll.find_one({ "addr": addr })
        if word_doc:
            word_doc['created'] = int(time.time())
            coll.save(word_doc)
        else:
            word_doc = { 'addr': addr, 'created': int(time.time()) }
            coll.insert(word_doc)
        # del word_doc["_id"]

        self.write(json_util.dumps(word_doc))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", QQHandler)]
        # conn = pymongo.Connection("localhost", 27017)
        conn = pymongo.MongoClient(host='mongodb://{username}:{password}@{host}:{port}/{dbname}'.format(**options.mongo_cfg))
        self.db = conn["mm-mc"]
        tornado.web.Application.__init__(self, handlers, debug=False)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
