"""opene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path(r'api/', include('otest.urls')),
    path(r'ms/', include('ms.urls')),
]

from django.conf import settings
if settings.DEBUG:
    from rest_framework.documentation import include_docs_urls
    urlpatterns += [
        path(r'docs/', include_docs_urls(title="U-Mail Web API", authentication_classes=[], permission_classes=[])),
        # drf 登录
        path(r'drf/', include('rest_framework.urls', namespace='rest_framework')),
    ]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
#
# from django.conf.urls.static import static
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
