# -*- coding: utf-8 -*-

import MySQLdb

db = MySQLdb.connect(
    host="localhost",    # 主机名
    port=4000,    # 端口
    user="dblog",         # 用户名
    passwd="123456",  # 密码
    db="dblog")        # 数据库名称

# 查询前，必须先获取游标
cur = db.cursor()

# 执行的都是原生SQL语句
cur.execute("SELECT * FROM blog_tag")

for row in cur.fetchall():
    print(row)

db.close()