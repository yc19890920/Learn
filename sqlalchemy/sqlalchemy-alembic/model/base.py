from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456@192.168.1.24:3306/sql_alembic?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Base = declarative_base()
