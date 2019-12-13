from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'test', views.TestViewset, base_name="TestViewset")
# router.register(r't', views.TestViewset, base_name="TestViewset2")

urlpatterns = [
    url(r'^', include(router.urls)),
]