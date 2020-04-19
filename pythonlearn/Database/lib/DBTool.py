# -*- coding: utf-8 -*-
#

import sys
import traceback
import time
import redis
import psycopg2
import MySQLdb
import pymongo
from DBUtils.PooledDB import PooledDB

from . import settings


############################################################
# 数据库对象
class DatabaseObj(object):

    def __init__(self):
        self.MysqlPool = None
        self.PgsqlPool = None
        self.Redis = None
        self.MongoConn = None
        self.MongoDBPool = None


# 数据库连接类
class DBToolKit(object):
    def __init__(self):
        # 数据库初始化参数列表
        self.db = DatabaseObj()
        self.error = sys.stderr.write

    ############################################################
    # 初始化数据库连接池
    def init_pool(self, dbtype, outerr=True):
        try:
            if dbtype=='edm_web':
                __DBPARAMS = settings.DATABASES['mysql']['edm_web']
                __DBPARAMS.update(creator=MySQLdb, charset='UTF8')
                self.db.MysqlPool = PooledDB(maxusage=1000, **__DBPARAMS)
            if dbtype=='mail_relay':
                __DBPARAMS = settings.DATABASES['postgresql']['mail_relay']
                __DBPARAMS.update(creator=psycopg2, failures=(psycopg2.InterfaceError, ))
                self.db.PgsqlPool = PooledDB(maxusage=1000, **__DBPARAMS)
        except BaseException as e:
            if outerr:
                sys.stderr.write('init %s pool except' % dbtype)
                sys.stderr.write(traceback.format_exc())
            return False
        return True

    # 取得数据库连接
    def __get_connect(self, dbtype):
        if dbtype=='edm_web': conn = self.db.MysqlPool.connection()
        if dbtype=='mail_relay': conn = self.db.PgsqlPool.connection()
        return conn

    # 查询数据库
    def query(self, dbtype, sql, args=None):
        # 取得数据库连接、游标
        conn = self.__get_connect(dbtype)
        cr = conn.cursor()
        # 执行查询，并取得结果
        cr.execute(sql, args)
        res = cr.fetchall()
        # 关闭游标、连接
        cr.close()
        conn.close()
        return res

    # 执行数据库操作
    def do(self, dbtype, sql, args=None):
        conn = self.__get_connect(dbtype)
        cr = conn.cursor()
        # 执行操作
        cr.execute(sql, args)
        cr.close()
        conn.close()
        return True

    # 执行数据库操作
    def doMany(self, dbtype, sql, args=None):
        conn = self.__get_connect(dbtype)
        cr = conn.cursor()
        # 执行操作
        cr.executemany(sql, args)
        # 关闭游标、数据库连接
        cr.close()
        conn.close()
        return True

    # 维护 数据库 连接
    def maintain_pool(self, dbtype, trycount=5, timeout=3) :
        i = 0
        while True:
            i += 1
            sys.stderr.write('try connect %s : %d' % (dbtype, i))
            try:
                conn = self.__get_connect(dbtype)
                break
            except BaseException, e:
                pass
            if i==trycount:
                sys.stderr.write('reconnect %s failure\n' % dbtype)
                self.error(traceback.format_exc())
                return False
            time.sleep(timeout)
        self.error('reconnect %s success' % dbtype)
        return conn

    ############################################################
    # 处理异常
    def process_exception(self, dbtype, e):
        if dbtype == 'edm_web' and type(e) == MySQLdb._mysql.OperationalError :
            return self.maintain_pool(dbtype)
        if dbtype == 'mail_relay' and type(e) in (psycopg2.OperationalError, psycopg2.InterfaceError) :
            return self.maintain_pool(dbtype)
        if dbtype == 'mongo' :
            return self.maintain_mongoPool()
        return False

    ############################################################
    # redis
    def __init_redis(self):
        __redis_pool = redis.ConnectionPool(
            host=settings.REDIS_SET['host'], port=settings.REDIS_SET['port'], db=0
        )
        self.db.Redis = redis.StrictRedis(connection_pool=__redis_pool)

    def get_redis_connection(self):
        self.__init_redis()
        return self.db.Redis

    ############################################################
    # MongoDB 操作
    # 初始化 MongoDB 连接
    def init_mongo(self, outerr=True):
        try:
            self.db.MongoConn = pymongo.Connection(
                settings.MONGODB_SET['host'],
                settings.MONGODB_SET['port'],
            )
            self.db.MongoDBPool = self.db.MongoConn[settings.MONGODB_SET['dbname']]
            self.db.MongoDBPool.authenticate(settings.MONGODB_SET['user'], settings.MONGODB_SET['pass'])
        except Exception, e :
            if outerr :
                self.error('init mongodb connect except')
                self.error(traceback.format_exc())
            return False
        return True

    # 取得 MongoDB 的 Collection 对象
    def get_mongo_collection(self, cname) :
        return self.db.MongoDBPool[cname]

    # 维护 MongoDB 连接
    def maintain_mongoPool(self, trycount=5) :
        self.error('maintain mongodb exception')
        i = 0
        while self.init_mongo(outerr=False) == False:
            i += 1
            self.error('try connect mongodb : %d' % i)
            if i == trycount :
                self.error('reconnect mongodb failure')
                self.error(traceback.format_exc())
                return False
            time.sleep(3)
        self.error('reconnect mongodb success')
        return True