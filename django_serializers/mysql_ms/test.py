import pymysql
import pprint

# 打开数据库连接
db = pymysql.connect(
    host='localhost',
    port=6033,
    password='123456',
    charset='utf8',
    # user='dblog',
    # db='dblog',

user='opene',
    db='test',
)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
# cursor.execute("select * from blog_category;")
cursor.execute("SELECT * FROM test")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

pprint.pprint(data)

# 关闭数据库连接
db.close()