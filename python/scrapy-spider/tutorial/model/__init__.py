# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc :
"""
import datetime
from contextlib import contextmanager

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from tutorial.settings import DATABASE


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))

def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)

def _get_date():
    return datetime.datetime.now()

Base = declarative_base()