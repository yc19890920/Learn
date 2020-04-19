#-*- coding: utf8 -*-

import sys
from lib.DBkit import getDBObject, get_redis_connection
from lib.settings import DATABASES

if __name__ == "__main__":

    sql = 'SELECT username FROM core_customer Limit 1;'
    mysql_obj = getDBObject('mysql', 'edm_web', DATABASES['mysql']['edm_web'])
    sql = 'SELECT username FROM core_customer Limit 1;'
    res = mysql_obj.query(sql)
    print res