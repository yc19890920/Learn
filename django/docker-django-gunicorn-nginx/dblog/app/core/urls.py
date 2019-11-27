# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.views import login, logout
from app.core import views
from app.core.forms import CustomizeAuthenticationForm

urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^login$', login,  {'template_name': 'core/login.html', 'authentication_form': CustomizeAuthenticationForm}, name='login'),
    url(r'^logout$', views.mylogout, name='logout'),
    # url(r'^logout$', logout, {'template_name': 'core/logout.html'}, name='logout'),
]