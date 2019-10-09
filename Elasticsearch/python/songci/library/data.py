#!-*- coding: utf-8 -*-

import hashlib
import os
import sqlite3
from .zh_conv import tradition2simple


def getMD5(data):
    if not data:
        return None
    data = data.encode("utf-8")
    md5obj = hashlib.md5()
    md5obj.update(data)
    hash = md5obj.hexdigest()
    return hash.lower()

def getPoetry():
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), "ci.db"))
    c = sqlite3.connect(path)
    cursor = c.execute("SELECT * from ci;")
    for row in cursor:
        id, title, auth, content = row
        # print (id, title, auth, content)
        title = tradition2simple(title)
        auth = tradition2simple(auth)
        content = tradition2simple(content)
        md5 = getMD5(content)
        yield ( md5, title, auth, content )