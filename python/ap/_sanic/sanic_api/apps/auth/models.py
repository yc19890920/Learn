import hashlib

class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id={})".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}

    def check_password(self, raw_password):
        """
        :param raw_password: str type, not unicode
        :return:
        """
        return hashlib.md5(raw_password).hexdigest() == self.password

# abcxyz
users = [User(1, "user1", '70fb874a43097a25234382390c0baeb3'), User(2, "user2", '70fb874a43097a25234382390c0baeb3')]
username_table = { u.username: u for u in users }
userid_table = { u.user_id: u for u in users }