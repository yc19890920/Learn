# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from app.blog.models import Tag, Category

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']