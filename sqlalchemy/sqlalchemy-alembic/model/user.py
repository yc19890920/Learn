from sqlalchemy import Column, Integer, VARCHAR, Index
from .base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32))
    password = Column(VARCHAR(32))
    email = Column(VARCHAR(32))

    __table_args__ = (
        Index('ix_user_pwd', 'username', 'password'),
        Index('ix_email_pwd', 'email', 'password'),
    )
