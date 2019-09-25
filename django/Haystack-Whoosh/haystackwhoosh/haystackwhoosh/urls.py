"""haystackwhoosh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from haystack.views import SearchView

from app.blog.models import Article

class MySeachView(SearchView):
    pass

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'^search/', include('haystack.urls')),
    path('blog/', include('app.blog.urls')),
    # 其实haystack.urls的内容为
    # url(r'^$', SearchView(), name='haystack_search'),
    url(r'^$', MySeachView(), name='haystack_search'),
]
