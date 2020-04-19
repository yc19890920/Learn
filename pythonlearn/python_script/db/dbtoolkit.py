# -*- coding: utf-8 -*-
#
import time
import traceback
import redis
import psycopg2
import MySQLdb
import pymongo
from DBUtils.PooledDB import PooledDB

############################################################
# 数据库对象
class DatabaseObject(object) :
    def __init__(self) :
        # dbname: mm-ms
        self.mysql_ms_pool = None
        # dbname: mm-pool
        self.mysql_pool_pool = None
        # dbname: mail_relay
        self.pgsql_pool = None

        self.conn_mongo = None
        self.db_mongo = None
        self.db_redis = None


# 数据库连接维护类
class DBToolKit(object):
    def __init__(self, param, logger):
        self.param  = param         # 参数列表
        self.log = logger           # 日志
        self.db = DatabaseObject()

    ############################################################
    # 异常处理
    # 输出异常信息
    def output_exception(self, e=None):
        self.log.error(traceback.format_exc())

    # 处理异常
    def process_exception(self, dbtype, e):
        res = False
        if dbtype == 'pgsql' and type(e) in (psycopg2.OperationalError, psycopg2.InterfaceError) :
            res = self.maintainDB(dbtype)
        if dbtype in ('mysql', 'mysql_pool') and type(e) == MySQLdb._mysql.OperationalError :
            res = self.maintainDB(dbtype)
        if dbtype == 'mongo' :
            res = self.maintainMongoDB()
        return res

    ############################################################
    # MySQL、PostgreSQL 操作
    # 初始化数据库地址池
    def initDBPool(self, dbtype, outerr=True) :

        # 数据库连接参数
        if dbtype == 'mysql' :
            DBPARAMS = {
                'creator'  : MySQLdb,
                'host'     : self.param['mysql']['host'],
                'port'     : int(self.param['mysql']['port']),
                'db'       : self.param['mysql']['dbname'],
                'charset'  : 'UTF8',
                'user'     : self.param['mysql']['user'],
                'passwd'   : self.param['mysql']['pass'],
            }
        # 数据库连接参数
        if dbtype == 'mysql_pool' :
            DBPARAMS = {
                'creator'  : MySQLdb,
                'host'     : self.param['mysql_pool']['host'],
                'port'     : int(self.param['mysql_pool']['port']),
                'db'       : self.param['mysql_pool']['dbname'],
                'charset'  : 'UTF8',
                'user'     : self.param['mysql_pool']['user'],
                'passwd'   : self.param['mysql_pool']['pass'],
            }
        if dbtype == 'pgsql' :
            DBPARAMS = {
                'creator'  : psycopg2,
                'host'     : self.param['pgsql']['host'],
                'port'     : int(self.param['pgsql']['port']),
                'dbname'   : self.param['pgsql']['dbname'],
                'user'     : self.param['pgsql']['user'],
                'password' : self.param['pgsql']['pass'],
                'failures' : (psycopg2.InterfaceError,)
            }

        # 连接数据库
        try:
            if dbtype == 'mysql' :
                self.db.mysql_ms_pool = PooledDB(maxusage=1000, **DBPARAMS)
            if dbtype == 'mysql_pool' :
                self.db.mysql_pool_pool = PooledDB(maxusage=1000, **DBPARAMS)
            if dbtype == 'pgsql' :
                self.db.pgsql_pool = PooledDB(maxusage=1000, **DBPARAMS)
        except Exception, e :
            if outerr :
                if dbtype == 'mysql' :
                    self.log.error( 'init mysql mm-ms pool exception')
                if dbtype == 'mysql_pool' :
                    self.log.error( 'init mysql mm-pool pool exception')
                if dbtype == 'pgsql' :
                    self.log.error('init postgresql pool exception')
                self.output_exception(e)
            return False
        return True

    # 查询数据库
    def DBQuery(self, dbtype, sql, args=None) :
        # 取得数据库连接、游标
        if dbtype == 'mysql' : db_conn = self.db.mysql_ms_pool.connection()
        if dbtype == 'mysql_pool' : db_conn = self.db.mysql_pool_pool.connection()
        if dbtype == 'pgsql' : db_conn = self.db.pgsql_pool.connection()
        db_cursor = db_conn.cursor()

        # 执行查询，并取得结果
        db_cursor.execute(sql, args)
        res = db_cursor.fetchall()

        # 关闭游标、连接
        db_cursor.close()
        db_conn.close()

        return res

        # try :
        #     # 取得数据库连接、游标
        #     if dbtype == 'mysql' : db_conn = self.db.mysql_ms_pool.connection()
        #     if dbtype == 'mysql_pool' : db_conn = self.db.mysql_pool_pool.connection()
        #     if dbtype == 'pgsql' : db_conn = self.db.pgsql_pool.connection()
        #     db_cursor = db_conn.cursor()
        #
        #     # 执行查询，并取得结果
        #     db_cursor.execute(sql, args)
        #     res = db_cursor.fetchall()
        #
        #     # 关闭游标、连接
        #     db_cursor.close()
        #     db_conn.close()
        #
        #     return res
        # except Exception, e :
        #     if self.maintainDB(dbtype) == False :
        #         return False
        #     return self.DBQuery(dbtype, sql, args)

    # 执行数据库操作
    def DBExecute(self, dbtype, sql, args=None):
        # 取得数据库连接、游标
        if dbtype == 'mysql' : db_conn = self.db.mysql_ms_pool.connection()
        if dbtype == 'mysql_pool' : db_conn = self.db.mysql_pool_pool.connection()
        if dbtype == 'pgsql' : db_conn = self.db.pgsql_pool.connection()
        db_cursor = db_conn.cursor()

        # 执行操作并取得结果
        res = db_cursor.execute(sql, args)

        # 关闭游标、数据库连接
        db_cursor.close()
        db_conn.close()

        return True
        # try :
        #     # 取得数据库连接、游标
        #     if dbtype == 'mysql' : db_conn = self.db.mysql_ms_pool.connection()
        #     if dbtype == 'mysql_pool' : db_conn = self.db.mysql_pool_pool.connection()
        #     if dbtype == 'pgsql' : db_conn = self.db.pgsql_pool.connection()
        #     db_cursor = db_conn.cursor()
        #
        #     # 执行操作并取得结果
        #     res = db_cursor.execute(sql, args)
        #
        #     # 关闭游标、数据库连接
        #     db_cursor.close()
        #     db_conn.close()
        #
        #     return True
        # except Exception, e :
        #     if self.maintainDB(dbtype) == False :
        #         return False
        #     return self.DBExecute(dbtype, sql, args)

    # 维护 数据库 连接
    def maintainDB(self, dbtype, trycount=5) :
        if   dbtype == 'mysql' :
            db_pool = self.db.mysql_ms_pool
            db_name = 'mysql'
        elif   dbtype == 'mysql_pool' :
            db_pool = self.db.mysql_pool_pool
            db_name = 'mysql_pool'
        elif dbtype == 'pgsql' :
            db_pool = self.db.pgsql_pool
            db_name = 'postgresql'
        self.log.error('%s exception' % db_name)
        i = 0
        while True:
            i += 1
            self.log.error('try connect %s : %d' % (db_name, i))
            try :
                db_conn = db_pool.connection()
                break
            except Exception, e :
                pass
            if i == trycount :
                self.log.error('reconnect %s failure\n' % db_name)
                self.output_exception()
                return False
            time.sleep(3)
        self.log.error('reconnect %s success' % db_name)
        return db_conn

    ############################################################
    # Redis 操作
    # 初始化 redis 连接
    def initRedisDB(self) :
        try:
            # 创建 redis 对象
            self.db.db_redis = redis.Redis(unix_socket_path=self.param['redis']['sock'])
            # 创建 redis 操作管道
            self.db.db_redis_pipe = self.db.db_redis.pipeline()
        except Exception, e:
            self.log.error('init redis connect exception')
            self.output_exception(e)
            return False
        return True


    ############################################################
    # MongoDB 操作
    # 初始化 MongoDB 连接
    def initMongoDB(self, outerr=True) :
        try:
            self.db.conn_mongo = pymongo.Connection(
                self.param['mongo']['host'],
                int(self.param['mongo']['port'])
            )
            self.db.db_mongo = self.db.conn_mongo[self.param['mongo']['dbname']]
            self.db.db_mongo.authenticate(self.param['mongo']['user'], self.param['mongo']['pass'])
        except Exception, e :
            if outerr :
                self.log.error('init mongodb connect exception')
                self.output_exception(e)
            return False
        return True


    # 取得 MongoDB 的 Collection 对象
    def getMongoDBCollection(self, c_name) :
        return self.db.db_mongo[c_name]

    # 维护 MongoDB 连接
    def maintainMongoDB(self, trycount=5) :
        self.log.error('maintain mongodb exception')
        i = 0
        while self.initMongoDB(outerr=False) == False:
            self.log.error('try connect mongodb : %d' % (i+1))
            i += 1
            if i == trycount :
                self.log.error('reconnect mongodb failure')
                self.output_exception()
                return False
            time.sleep(3)
        self.log.error('reconnect mongodb success')
        return True
