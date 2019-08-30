# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^home/$', views.home, name='home'),
]
