# -*- coding:utf-8 -*-
#

import tornado.gen

@tornado.gen.engine
def query_user(db, username, callback=None):
    sql = "SELECT `username`, `password`, `email` FROM `core_customer` WHERE `username`= %s;"
    args = (username, )
    res = db.query(sql, args)
    callback(res)