#-*- coding: utf8 -*-

import redis
import psycopg2
import MySQLdb
import DBUtils.PooledDB

from . import settings

___Mysql_Params = settings.DATABASES['mysql']['edm_web']
__MysqlPool = DBUtils.PooledDB.PooledDB(MySQLdb, 1, charset='utf8', **___Mysql_Params)

___Pgsql_Params = settings.DATABASES['postgresql']['mail_relay']
__PgsqlPool = DBUtils.PooledDB.PooledDB(psycopg2, 1, **___Pgsql_Params)


redis_pool = redis.ConnectionPool(
    host=settings.REDIS_SET['host'], port=settings.REDIS_SET['port'], db=0
)
redis = redis.StrictRedis(connection_pool=redis_pool)

def __get_connect(dbname):
    if dbname == 'edm_web':
        return __MysqlPool.connection()
    elif dbname == 'mail_relay':
        return __PgsqlPool.connection()
    return None

def query(dbname, sql, args=()):
    conn = __get_connect(dbname)
    cr = conn.cursor()
    cr.execute(sql, args)
    res = cr.fetchall()
    cr.close()
    conn.close()
    return res

def do(dbname, sql, args=()):
    conn = __get_connect(dbname)
    cr = conn.cursor()
    cr.execute(sql, args)
    conn.commit()
    cr.close()
    conn.close()
    return True

def doMany(dbname, sql, args=[]):
    conn = __get_connect(dbname)
    cr = conn.cursor()
    cr.executemany(sql, args)
    conn.commit()
    cr.close()
    conn.close()
    return True
