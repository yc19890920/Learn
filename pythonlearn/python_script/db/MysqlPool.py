# -*- coding: UTF-8 -*-
"""
Created on 2016年5月7日
@author: baocheng
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    #连接池对象
    __pool = None
    def __init__(self, param, logger):
        #数据库构造函数，从连接池中取出连接，并生成操作游标
        DBPARAMS = {
            'creator'  : MySQLdb,
            'host'     : param['mysql']['host'],
            'port'      : int(param['mysql']['port']),
            'db'        : param['mysql']['dbname'],
            'charset'  : 'UTF8',
            'user'     : param['mysql']['user'],
            'passwd'   : param['mysql']['pass'],
        }
        self.logger = logger
        self._conn = Mysql.__getConn(**DBPARAMS)
        self._cursor = self._conn.cursor()
        self.logger.info(u'init mysql pool success.')

    @staticmethod
    def __getConn(**DBPARAMS):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection

        dbapi ：数据库接口
        mincached ：启动时开启的空连接数量
        maxcached ：连接池最大可用连接数量
        maxshared ：连接池最大可共享连接数量
        maxconnections ：最大允许连接数量
        blocking ：达到最大数量时是否阻塞
        maxusage ：单个连接最大复用次数

        dbapi: 需要使用的DB-API 2模块
        mincached : 启动时开启的空连接数量(缺省值 0 意味着开始时不创建连接)
        maxcached: 连接池使用的最多连接数量(缺省值 0 代表不限制连接池大小)
        maxshared: 最大允许的共享连接数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量，被请求为共享的连接将会被共享使用。
        maxconnections: 最大允许连接数量(缺省值 0 代表不限制)
        blocking: 设置在达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误；其他代表阻塞直到连接数减少)
        maxusage: 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用)。当达到最大数值时，连接会自动重新连接(关闭和重新打开)
        setsession: 一个可选的SQL命令列表用于准备每个会话，如 ["set datestyle to german", ...]
        其他，你可以设置用于传递到真正的DB-API 2的参数，例如主机名、数据库、用户名、密码等。
        """
        if Mysql.__pool is None:
            __pool = PooledDB(maxusage=1000, **DBPARAMS)
            # __pool = PooledDB(creator=MySQLdb, mincached=20, maxcached=20,
            #                   host=Config.DBHOST, port=Config.DBPORT, user=Config.DBUSER, passwd=Config.DBPWD,
            #                   db=Config.DBNAME, use_unicode=False, charset=Config.DBCHAR, cursorclass=DictCursor)
        return __pool.connection()

    def getAll(self,sql,param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self,sql,param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self,sql,num,param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self,sql,value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql,value)
        return self.__getInsertId()

    def insertMany(self,sql,values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql,values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self,sql,param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        return count

    def update(self,sql,param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)

    def delete(self,sql,param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self,option='commit'):
        """
        @summary: 结束事务
        """
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self,isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cursor.close()
        self._conn.close()
        self.logger.info(u'close mysql pool success.')
