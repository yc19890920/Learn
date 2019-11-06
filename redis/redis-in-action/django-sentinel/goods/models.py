# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Goods(models.Model):
    """ 系统配置
    """
    num = models.IntegerField(u'商品数量', default=0)
    version = models.IntegerField(u'值', default=0)


    class Meta:
        managed = False
        db_table = 'goods'
