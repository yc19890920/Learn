# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters

from app.rest.serializers import TagSerializer, CategorySerializer
from app.blog.models import Tag, Category


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('name')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'name')