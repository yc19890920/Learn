import sys
import hashlib
from django.db import models
from django.db import connection

class Tag(models.Model):
    """ tag(标签云)对应的数据库
    """
    name = models.CharField('标签名', max_length=20, unique=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)
    count = models.IntegerField('数量', default=0)

    class Meta:
        db_table = 'ms_tag'
        ordering = ['name']
        verbose_name = '标签'

class Category(models.Model):
    """ 另外一个表,储存文章的分类信息
    文章表的外键指向
    """
    name = models.CharField('类名', max_length=20, unique=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'ms_category'
        ordering = ['name']
        verbose_name = '分类'


class Article(models.Model):
    title = models.CharField('标题', max_length=100, null=False, blank=False, db_index=True)
    content = models.TextField('正文', null=False, blank=False)
    tag = models.ForeignKey(Tag, verbose_name=u'标签', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, verbose_name=u'分类', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)
    count = models.IntegerField('数量', default=0)

    class Meta:
        db_table = 'ms_article'
        verbose_name = u'文章'


##################################################################
# 分表 方案一： 态创建数据库表，并元类方式映射数据模型。（动态创建模型，动态使用模型）
def get_user_model(hashID):

    class UserMetaClass(models.base.ModelBase):

        def __new__(cls, name, bases, attrs):
            """
            model._meta:
             ['FORWARD_PROPERTIES', 'REVERSE_PROPERTIES', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
             '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
             '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
             '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_expire_cache',
             '_forward_fields_map', '_get_fields', '_get_fields_cache', '_ordering_clash',
             '_populate_directed_relation_graph', '_prepare', '_property_names', '_relation_tree', 'abstract',
             'add_field', 'add_manager', 'app_config', 'app_label', 'apps', 'auto_created', 'auto_field',
             'base_manager', 'base_manager_name', 'can_migrate', 'concrete_fields', 'concrete_model',
             'contribute_to_class', 'db_table', 'db_tablespace', 'default_apps', 'default_manager',
             'default_manager_name', 'default_permissions', 'default_related_name', 'fields', 'fields_map',
             'get_ancestor_link', 'get_base_chain', 'get_field', 'get_fields', 'get_latest_by', 'get_parent_list',
             'get_path_from_parent', 'get_path_to_parent', 'index_together', 'indexes', 'installed', 'label',
             'label_lower', 'local_concrete_fields', 'local_fields', 'local_managers', 'local_many_to_many', 'managed',
             'managers', 'managers_map', 'many_to_many', 'model', 'model_name', 'object_name', 'order_with_respect_to',
             'ordering', 'original_attrs', 'parents', 'permissions', 'pk', 'private_fields', 'proxy', 'proxy_for_model',
             'related_fkey_lookups', 'related_objects', 'required_db_features', 'required_db_vendor', 'select_on_save',
             'setup_pk', 'setup_proxy', 'swappable', 'swapped', 'unique_together', 'verbose_name',
             'verbose_name_plural', 'verbose_name_raw']
            """
            model = super().__new__(cls, name, bases, attrs)
            model._meta.app_label = 'ms'
            model._meta.model_name = 'user_{}'.format(hashID)
            model._meta.db_table = 'user_{}'.format(hashID)
            model._meta.verbose_name = "用户表"
            return model

    class User(models.Model, metaclass=UserMetaClass):
        username = models.CharField(u'用户名', max_length=64, null=False, blank=False, unique=True)
        email = models.CharField(u'邮箱', max_length=100, null=False, blank=False, db_index=True)
        created = models.DateTimeField('创建时间', auto_now_add=True)
        updated = models.DateTimeField('修改时间', auto_now=True)

        def __str__(self):
            return self.username

    return User

def install_user_model(hashID):
    cr = connection.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS `user_{0}` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `username` varchar(64) NOT NULL,
      `email` varchar(200) NOT NULL,
      `created` datetime(6) NOT NULL,
      `updated` datetime(6) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `username` (`username`),
      KEY `user_{0}_email` (`email`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """.format(hashID)
    cr.execute(sql)

def get_hashID(username, hashMode=64, tableGroup=4):
    """根据 username 确定唯一 hash 值（确定分表）
     # 分组公式：64 = 每组多少个count  * group需要分组的个数
     # 数据所在环的位置（也就是在哪个库中）：value = key mode 64 / count  * count

    hash(key)在0~3之间在第0号表
    hash(key)在4~7之间在第4号表
    hash(key)在8~11之间在第8号表

    hash(key)在0~3之间在第0号库
    hash(key)在4~7之间在第4号库
    hash(key)在8~11之间在第8号库
    """
    # hash = int
    username = str(username).lower()
    hashID = int(hash(username) % hashMode / tableGroup )
    return hashID
    # # 16进制 -- 900150983cd24fb0d6963f7d28e17f72
    # hash_str = hashlib.md5(username.lower().encode(encoding='UTF-8')).hexdigest()
    # userId = int(hash_str, 16)  # 16进制 --> 10进制
    # # print(hash_str, hash_str[:2], hash_str[-2:], num)
    # # 按hashCount个为一组，分4个表
    # hashID = int(hash(username) % hashMode / tablePiece)
    # # hashID = num % hashNum
    # # print('HashID:', hashID)
    # return hashID

def create_user_model(username):
    # 调用 hashID, 确定 分表id
    table_id = get_hashID(username)
    model = get_user_model(table_id)
    install_user_model(table_id)
    return model


##################################################################
# 分表 方案二： 直接路由写死模型，根据路由规则代理到不同模型。
# 表分片的数量
SHARD_TABLE_NUMBER = 2

class User(models.Model):
    username = models.CharField(u'用户名', max_length=64, null=False, blank=False, unique=True)
    email = models.CharField(u'邮箱', max_length=100, null=False, blank=False, db_index=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True

class User1(User):
    class Meta:
        db_table = 'myuser_1'

class User2(User):
    class Meta:
        db_table = 'myuser_2'

def get_sharding_model(username):
    table_id = get_hashID(username, hashMode=2, tableGroup=1)
    if table_id == 0:
        return User1
    elif table_id == 1:
        return User2