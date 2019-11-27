# -*- coding: utf-8 -*-
from django.conf.urls import url
from app.blog import blogviews as views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^p/(?P<article_id>\d+)/$', views.detail, name='detail'),
    url(r'^s/$', views.search, name='search'),
    url(r'^t/(?P<tag_id>\d+)/$', views.tag, name='tag'),
    url(r'^score/$', views.score, name='score'),

    # url(r"^category/(?P<cate_id>\d+)/$", views.category, name='category'),
    # url(r'^thanks/$', views.thanks, name='thanks')
]