from sqlalchemy.ext.declarative import declarative_base
from aiomysql.sa import create_engine

from sqlalchemy import Column, Integer, VARCHAR, Index, Text, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship


class Db(object):
    Column = Column
    Integer = Integer
    VARCHAR = VARCHAR
    String = String
    DateTime = DateTime
    Index = Index
    Text = Text
    ForeignKey = ForeignKey
    relationship = relationship

    def __init__(self):
        self.Model = declarative_base()
        self.engine = None

    async def init_engine(self, *args, **kwargs):
        self.engine = await create_engine(*args, **kwargs)


db = Db()
