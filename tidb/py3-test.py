import pymysql
conn = pymysql.connect(host='127.0.0.1', port=4000, user='root', passwd="xxx", db='mysql')
cur = conn.cursor()
# cur.execute("SELECT Host,User FROM user")
cur.execute("SELECT * FROM blog_tag")
for r in cur:
    print(r)
cur.close()
conn.close()


# 4、peewee
# 写原生 SQL 的过程非常繁琐，代码重复，没有面向对象思维，继而诞生了很多封装 wrapper 包和 ORM 框架，
# ORM 是 Python 对象与数据库关系表的一种映射关系，有了 ORM 你不再需要写 SQL 语句。提高了写代码的速度，
# 同时兼容多种数据库系统，如sqlite, mysql、postgresql，付出的代价可能就是性能上的一些损失。
# 如果你对 Django 自带的 ORM 熟悉的话，那么 peewee的学习成本几乎为零。它是 Python 中是最流行的 ORM 框架。
#
# pip install peewee
# 一个例子
#
# import peewee
# from peewee import *
#
# db = MySQLDatabase('jonhydb', user='john', passwd='megajonhy')
#
# class Book(peewee.Model):
#     author = peewee.CharField()
#     title = peewee.TextField()
#
#     class Meta:
#         database = db
#
# Book.create_table()
# book = Book(author="me", title='Peewee is cool')
# book.save()
# for book in Book.filter(author="me"):
#     print(book.title)
# 官方文档：http://docs.peewee-orm.com/en/latest/peewee/installation.html




# 5、SQLAlchemy
# 如果想找一种既支持原生 SQL，又支持 ORM 的工具，那么 SQLAlchemy 是最好的选择，它非常接近 Java 中的 Hibernate 框架。
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from sqlalchemy_declarative import Address, Base, Person
#
# class Address(Base):
#     __tablename__ = 'address'
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#
# engine = create_engine('sqlite:///sqlalchemy_example.db')
# Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
#
# # Insert a Person in the person table
# new_person = Person(name='new person')
# session.add(new_person)
# session.commit()
# 现在差不多搞明白了这几种数据库驱动的优劣，接下来你就可以选择其中的一个进行系统的学习再把它应用到项目中去了，祝你学习开心，不懂的可以咨询我哈。


