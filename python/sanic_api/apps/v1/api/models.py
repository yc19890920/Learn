import datetime
from apps.db import db
from peewee import CharField, DateTimeField, TextField, Model

class BaseModel(Model):
    class Meta:
        database = db
        indexes = (
            # create a no-unique on username and email
            (('sex', 'email'), False),
        )

    @classmethod
    def filters(cls, sex=None, email=None, username=None, page_number=1, items_per_page=20):
        """this filter code for example demo"""
        qs = cls.select()
        if sex:
            qs = qs.where(cls.sex == sex)
        if email:
            qs = qs.where(cls.email.contains(email))
        if username:
            qs = qs.where(cls.username.contains(username))
        cls.result = qs.order_by(cls.id).paginate(page_number, items_per_page)
        return cls

    @classmethod
    def counts(cls):
        return cls.result.count()

    @classmethod
    def values_list(cls, *args, **kwargs):
        result = []
        for arg in args:
            qs_expression = "{0}.select({0}.{1}).iterator()".format(cls.__name__, arg)
            for row in eval(qs_expression):
                result.append(eval('row.{0}'.format(arg)))
        return result


class ShanghaiPersonInfo(BaseModel):
    create_datetime = DateTimeField(default=datetime.datetime.utcnow(), null=True)
    username = CharField()
    email = CharField()
    phone = CharField()
    sex = CharField()
    zone = TextField()

    def model_to_dict(self):
        data = self.__data__.copy()
        try: del data['id']
        except: pass
        return data