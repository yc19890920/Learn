import os
import sys
import pymysql
import logging
import django
import traceback
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../haystackwhoosh')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "haystackwhoosh.settings")
django.setup()
from app.blog.models import Article

_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
log = logging.getLogger('office')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

# 打开数据库连接
db = pymysql.connect("localhost", "dblog", "123456", "dblog")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("select title, content, views, likes, auth, source, created, updated from blog_article")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
for title, content, views, likes, auth, source, created, updated in data:
    log.info("同步主题：%s" % title)
    print("同步主题：%s" % title)
    Article.objects.create(
        title=title, content=content, views=views, likes=likes, auth=auth, source=source, created=created, updated=updated
    )

# print("Database version : %s " % data)

# 关闭数据库连接
db.close()