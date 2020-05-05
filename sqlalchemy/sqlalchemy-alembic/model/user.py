import datetime
from sqlalchemy import Column, Integer, VARCHAR, Index, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(32), unique=True)
    email = Column(VARCHAR(32))
    password = Column(VARCHAR(32))

    items = relationship("Item", back_populates="owner")

    __table_args__ = (
        Index('ix_user_pwd', 'username', 'password'),
        Index('ix_email_pwd', 'email', 'password'),
    )

    def __str__(self):
        return "<User(username='%s', femail='%s')>" % (
            self.username, self.email)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(100), index=True, nullable=False, doc="主题")
    description = Column(Text, nullable=True, doc="描述")
    owner_id = Column(Integer, ForeignKey("user.id"), doc="用户ID")
    created = Column(DateTime, nullable=True, default=datetime.datetime.now(), doc="创建时间")
    updated = Column(DateTime, nullable=True, default=datetime.datetime.now(), doc="修改时间")

    owner = relationship("User", back_populates="items")

    def __str__(self):
        return "<Item(title='%s')>" % (self.title)
