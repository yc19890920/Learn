# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models

# Create your models here.


class User(models.Model):
    # key是保留字
    password = models.IntegerField()
    nick = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    # create_time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'demo_user'
