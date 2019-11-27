# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from app.core.choices import GENDER


class User(AbstractUser):
    """ 继承 AbstractUser
    字段 id, username, password, last_login, date_joined, first_name, last_name, email, is_staff, is_active, is_superuser
    is_staff:   Designates whether the user can log into this admin site.  指示用户是否可以访问Admin 站点。
    is_active: Designates whether this user should be treated as active. Unselect this instead of deleting accounts.  指示用户的账号是否激活。
    is_superuser： 这个用户拥有所有的权限而不需要给他们分配明确的权限。
    """

    age = models.IntegerField(u"年龄", default=0)
    linkman = models.CharField(u'联系人', max_length=50, null=True, blank=True)
    phone = models.CharField(u"手机", max_length=20, null=True, blank=True)
    company = models.CharField(u"公司", max_length=50, null=True, blank=True)
    gender = models.CharField(u"性别", max_length=10, choices=GENDER, default="Male", null=False, blank=False)
    website = models.CharField(u"个人网址", max_length=200, null=True, blank=True)
    note = models.TextField(u"个性签名", null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = "core_user"


class Prefs(models.Model):
    """ 系统配置
    """
    name = models.CharField(u'键', max_length=30, null=False, blank=False, unique=True)
    value = models.TextField(u'值', null=True, blank=True)
    remark = models.TextField(u'描述', null=True, blank=True)

    class Meta:
        # managed = False
        db_table = 'core_prefs'

    def __str__(self):
        return self.value

    @staticmethod
    def getObj(name):
        obj, _created = Prefs.objects.get_or_create(name=name)
        return obj

    @staticmethod
    def geValue(name):
        return Prefs.getObj(name).value

    @staticmethod
    def saveValue(name, value=None, remark=None):
        obj = Prefs.getObj(name)
        obj.value = value
        obj.remark = remark
        obj.save()

class Department(models.Model):
    """
    部门信息
    """
    parent_id = models.IntegerField(u'父ID', default=0, db_index=True)
    name = models.CharField(u'名称', max_length=100, null=False, blank=False, unique=True)
    order = models.IntegerField(default=0, help_text=u"部门展现顺序")

    class Meta:
        db_table = 'core_department'

    def __str__(self):
        return self.name

    @property
    def next_id(self):
        return self.parent_id if self.parent_id>0 else 0

    @property
    def level(self, level=0):
        return Department.loopDepartLevel(self, level)

    @staticmethod
    def loopDepartLevel(obj, level):
        if obj.parent_id:
            return level
        level += 1
        next_obj = Department.objects.filter(id=obj.parent_id).first()
        return Department.loopDepartLevel(next_obj, level)
