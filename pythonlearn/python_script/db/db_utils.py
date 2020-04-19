#-*- coding: utf8 -*-

import os
import MySQLdb
import psycopg2
import DBUtils.PooledDB
import ConfigParser
import redis


cfg = ConfigParser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), '..', 'conf', 'config.conf'))

mysql_params = dict(cfg.items('mysql'))
mysql_params['port'] = int(mysql_params['port'])
if 'pass' in mysql_params:
    mysql_params['passwd'] = mysql_params.pop('pass')
if 'dbname' in mysql_params:
    mysql_params['db'] = mysql_params.pop('dbname')
mysql_pool = DBUtils.PooledDB.PooledDB(MySQLdb, 1, **mysql_params)

pgsql_params = dict(cfg.items('pgsql'))
pgsql_params['port'] = int(pgsql_params['port'])
if 'pass' in pgsql_params:
    pgsql_params['password'] = pgsql_params.pop('pass')
if 'dbname' in mysql_params:
    pgsql_params['dbname'] = pgsql_params.pop('dbname')
pgsql_pool = DBUtils.PooledDB.PooledDB(psycopg2, 1, **pgsql_params)


redis_db = redis.Redis(
    host=cfg.get('redis', 'host'),
    port=cfg.getint('redis', 'port')
)
# redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# redis = redis.StrictRedis(connection_pool=redis_pool)

def _get_conn(db_type):
    if db_type == 'mysql':
        return mysql_pool.connection()
    elif db_type == 'pgsql':
        return pgsql_pool.connection()
    return None

def query(db_type, sql, args=()):
    conn = _get_conn(db_type)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    rs = cursor.fetchall()
    cursor.close()
    conn.close()
    return rs


def do(db_type, sql, args=()):
    conn = _get_conn(db_type)
    cursor = conn.cursor()
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()
    return True


def doMany(db_type, sql, args=[]):
    conn = _get_conn(db_type)
    cursor = conn.cursor()
    cursor.executemany(sql, args)
    conn.commit()
    cursor.close()
    conn.close()
    return True
