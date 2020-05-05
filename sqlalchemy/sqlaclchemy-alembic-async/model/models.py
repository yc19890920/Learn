from datetime import datetime
from .base import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(32), unique=True)
    email = db.Column(db.VARCHAR(32))
    password = db.Column(db.VARCHAR(32))

    items = db.relationship("Item", back_populates="owner")

    __table_args__ = (
        db.Index('ix_user_pwd', 'username', 'password'),
        db.Index('ix_email_pwd', 'email', 'password'),
    )

    def __str__(self):
        return "<User(username='%s', femail='%s')>" % (
            self.username, self.email)


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(100), index=True, nullable=False, doc="主题")
    description = db.Column(db.Text, nullable=True, doc="描述")
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), doc="用户ID")
    created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow(), doc="创建时间")
    updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow(), doc="修改时间")

    owner = db.relationship("User", back_populates="items")

    def __str__(self):
        return "<Item(title='%s')>" % (self.title)
