# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.blog.blogurls import urlpatterns as blog_urls
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^core/', include('app.core.urls')),
    url(r'^core/set/', include('app.setting.urls')),
    url(r'^core/blog/', include('app.blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('app.rest.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += blog_urls

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns