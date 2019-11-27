# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.six import iteritems, integer_types
from .models import LogEntry, AuditlogContentype, AUDITLOG_EXTEND_TYPE

log = logging.getLogger('django')

def api_create_admin_log(request, instance, extend_type, extend_content, action=1):
    if extend_type not in dict(AUDITLOG_EXTEND_TYPE):
        raise TypeError(u" log_type not in AUDITLOG_EXTEND_TYPE or AUDITLOG_EXTEND_TYPE in settings;"
                        u"data like AUDITLOG_EXTEND_TYPE = ( ('login', _(u'登录')), ('logout', _(u'登出')),). ")

    if action not in dict(LogEntry.Action.choices):
        raise TypeError(u" extend_type not in AUDITLOG_EXTEND_TYPE or AUDITLOG_EXTEND_TYPE not in settings;"
                        u"data like AUDITLOG_EXTEND_TYPE = ( ('login', _(u'登录')), ('logout', _(u'登出')),). ")

    additional_data = changes = {}
    ctype = ContentType.objects.get_for_model(instance)
    pk = instance.pk
    object_id = 0
    if isinstance(pk, integer_types):
        object_id = pk

    AuditlogContentype.objects.get_or_create(content_type=ctype)
    LogEntry.objects.create(
        content_type=ctype, object_pk=pk, object_id=object_id, object_repr=smart_text(instance),
        action=action, changes=json.dumps(changes), actor=request.user, remote_addr=request.META['REMOTE_ADDR'],
        additional_data=additional_data,
        is_extend=True, extend_type=extend_type, extend_content=extend_content
    )
    return True





