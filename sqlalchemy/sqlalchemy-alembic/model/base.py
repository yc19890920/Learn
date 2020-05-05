from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456@192.168.1.24:3306/sql_alembic?charset=utf8"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlclient://root:123456@192.168.1.24:3306/sql_alembic?charset=utf8"
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:123456@192.168.1.24:3306/sql_alembic?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
