from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tag', views.TagViewset, base_name="TagViewset")
router.register(r'category', views.CategoryViewset, base_name="CategoryViewset")
router.register(r'article', views.ArticleViewset, base_name="ArticleViewset")
router.register(r'user', views.UserViewset, base_name="UserViewset")

urlpatterns = [
    url(r'^', include(router.urls)),
]