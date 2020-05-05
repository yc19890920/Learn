from sqlalchemy import Column, Integer, VARCHAR
from .base import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', VARCHAR(32))