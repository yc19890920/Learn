# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from goods.views import init, index1, index2

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^i$', init, name='init'),
    url(r'^i1$', index1, name='index1'),
    url(r'^i2$', index2, name='index2'),
]
urlpatterns += staticfiles_urlpatterns()

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)