from django.conf.urls import url
from app.blog import views

urlpatterns = [
    url(r'^p/(?P<article_id>\d+)/$', views.detail, name='article_detail'),
]