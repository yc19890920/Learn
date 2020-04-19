from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from app.rest import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customers', views.UserViewSet)

urlpatterns = [
    url(r'^$', login_required(router.get_api_root_view()), name=router.root_view_name),
    url(r'', include(router.urls))
]