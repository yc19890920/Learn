# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.contrib.auth.views import deprecate_current_app
from django.views.decorators.cache import never_cache
# from django.shortcuts import resolve_url
# from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.http import HttpResponseRedirect, QueryDict
# from django.template.response import TemplateResponse
# from django.utils.translation import ugettext as _
from .tasks import get_tcp_connect_info, get_network_monitor_info

@login_required
def home(request, template_name='core/home.html'):
    ntcp_info_json, bntcp_info_json = get_tcp_connect_info()
    network_monitor_keys, network_monitor_infos = get_network_monitor_info()
    return render(request, template_name, context={
        "ntcp_info_json": ntcp_info_json,
        "bntcp_info_json": bntcp_info_json,
        "network_monitor_infos": network_monitor_infos,
        "network_monitor_keys": network_monitor_keys,
    })

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

@deprecate_current_app
@never_cache
def mylogout(request):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

    # if next_page is not None:
    #     next_page = resolve_url(next_page)
    # elif settings.LOGOUT_REDIRECT_URL:
    #     next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
    #
    # if (redirect_field_name in request.POST or
    #         redirect_field_name in request.GET):
    #     next_page = request.POST.get(redirect_field_name,
    #                                  request.GET.get(redirect_field_name))
    #     # Security check -- don't allow redirection to a different host.
    #     if not is_safe_url(url=next_page, host=request.get_host()):
    #         next_page = request.path
    #
    # if next_page:
    #     # Redirect to this page until the session has been cleared.
    #     return HttpResponseRedirect(next_page)
    #
    # current_site = get_current_site(request)
    # context = {
    #     'site': current_site,
    #     'site_name': current_site.name,
    #     'title': _('Logged out')
    # }
    # if extra_context is not None:
    #     context.update(extra_context)
    #
    # return TemplateResponse(request, template_name, context)
