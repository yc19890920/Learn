# -*- coding: utf-8 -*-

from django.conf.urls import url
from app.setting import views

urlpatterns = [
    url(r'^$', views.systemSet, name='system_set'),
    url(r'^cfilter/$', views.cfilter, name='cfilter_set'),
    url(r'^cfilter/ajax$', views.ajax_cfilter, name='ajax_cfilter_set'),
    url(r'^cfilter/add/$', views.cfilter_add, name='cfilter_add_set'),
    url(r'^cfilter/(?P<rule_id>\d+)/$', views.cfilter_modify, name='cfilter_modify_set'),
    url(r'^cfilter/v/(?P<rule_id>\d+)/$', views.cfilter_view, name='cfilter_view_set'),
]