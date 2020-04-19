
# MySQL

````
import MySQLdb

conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
cr=conn.cursor()
cr.execute('select * from user')
cr.close()
conn.close()

````


## 乱码问题：
```
conn = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='python') 中加一个属性：
 改为：
conn = MySQLdb.Connect(host='localhost', user='root', passwd='root', db='python',charset='utf8') 
charset是要跟你数据库的编码一样，如果是数据库是gb2312 ,则写charset='gb2312'。
```
 
## 常用函数
> **1. Python DB API 2.0 对事务提供了两个方法：**
>> - `commit()` 提交
>> - `rollback()` 回滚
> **2. cursor用来执行命令的方法:**
>> `callproc(self, procname, args)`  用来执行存储过程,接收的参数为存储过程名和参数列表,返回值为受影响的行数
>> `execute(self, query, args)`      执行单条sql语句,接收的参数为sql语句本身和使用的参数列表,返回值为受影响的行数
>> `executemany(self, query, args)`  执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数
>> `nextset(self)`                   移动到下一个结果集
> **3. cursor用来接收返回值的方法:**
>> `fetchall(self)`              接收全部的返回结果行.
>> `fetchmany(self, size=None)`  接收size条返回结果行.如果size的值大于返回的结果行的数量,则会返回cursor.arraysize条数据.
>> `fetchone(self)`              返回一条结果行.
>> `scroll(self, value, mode='relative')`  移动指针到某一行.如果mode='relative',则表示从当前所在行移动value条,如果 mode='absolute',则表示从结果集的第一行移动value条.


## 其他
- [解决mysqldb查询大量数据导致内存使用过高的问题](http://blog.csdn.net/jianhong1990/article/details/41209493)
- [MySQLdb取回大结果集的技巧](http://www.jinglingshu.org/?p=3748)
- 在python3下，MySQLdb模块不再提供支持，此时可以使用另一个模块PyMySQL，它支持python2和python3。


## 文档
- [python操作mysql数据库](http://www.runoob.com/python/python-mysql.html)
- [python操作MySQL数据库](http://www.cnblogs.com/rollenholt/archive/2012/05/29/2524327.html)
- [Python连接MySQL数据库](http://www.jianshu.com/p/76fab6cb06f9)
- [MySql 正则表达式（查询非字符数字的记录）](https://zhuanlan.zhihu.com/p/28910674)
