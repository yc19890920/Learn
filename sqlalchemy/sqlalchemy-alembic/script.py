from model import User, Item
from model import Role
from model import SessionLocal
from sqlalchemy import and_, or_, all_, any_
from sqlalchemy import func

db = SessionLocal()


class UserFunc:
    @staticmethod
    def get_user(db: SessionLocal, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: SessionLocal, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(db: SessionLocal, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: SessionLocal, username: str = None, email: str = None, password: str = None):
        fake_password = password + "notreallyhashed"
        db_user = User(username=username, email=email, password=fake_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class ItemFunc:
    @staticmethod
    def get_items(db: SessionLocal, skip: int = 0, limit: int = 100):
        return db.query(Item).offset(skip).limit(limit).all()

    @staticmethod
    def get_user_items(db: SessionLocal, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Item).filter_by(owner_id=user_id).offset(skip).limit(limit).all()

    @staticmethod
    def create_user_item(db: SessionLocal, item: dict, user_id: int):
        db_item = Item(**item, owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


# # 创建用户
# user = UserFunc.create_user(db, username="yc", email="yc@test.com", password="123456")
# print(user, user.id)
#
# # 获取所有用户
# users = UserFunc.get_users(db)
# print(users)
#
# # 通过ID获取用户
# user2 = UserFunc.get_user(db, user.id)
# print(user2, user2.id)

# 通过email获取用户
user = UserFunc.get_user_by_email(db, email="yc@test.com")
print(user, user.id)

# 给用户添加items
itmes = [
    {'title': "1", "description": '1'},
    {'title': "2", "description": '2'},
    {'title': "3", "description": '3'},
]
# for item in itmes:
#     ItemFunc.create_user_item(db, item, user3.id)

## 获取所有items
itmes2 = ItemFunc.get_items(db)
print(itmes2)

# 获取所有用户
for i in user.items:
    print(i, i.owner.email)

print("=================")
## 获取某个用户下面的 item
itmes3 = ItemFunc.get_user_items(db, user.id)
print(itmes3)
for i in itmes3:
    print(i, i.owner.email)
