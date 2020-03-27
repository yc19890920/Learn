# -*- encoding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime

from tutorial.model import Base

class HuXiuModel(Base):
    """ 虎嗅网 表 """
    __tablename__ = 't_huxiu'

    id = Column(Integer, primary_key=True)
    link = Column(String(300), unique=True)
    title = Column(String(100))
    desc = Column(Text, nullable=True)
    published = Column(String(30), nullable=True)