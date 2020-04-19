# -*- coding: utf-8 -*-


############## Mysql

# host=127.0.0.1
# port=3306
# user=tornado
# passwd=tornado123
# dbname=tornado_test

from sqlalchemy import create_engine, MetaData, \
    Table, Column, Integer, String, ForeignKey


# echo=True 打印调试信息
engine = create_engine('mysql+mysqldb://tornado:tornado123@127.0.0.1/tornado_test', echo=True)
metadata = MetaData(engine)

user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(50)),
                   Column('fullname', String(100))
                   )

address_table = Table('address', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('user_id', None, ForeignKey('user.id')),
                      Column('email', String(128), nullable=False)
                      )

# create(bind=None, checkfirst=False)
metadata.create_all()