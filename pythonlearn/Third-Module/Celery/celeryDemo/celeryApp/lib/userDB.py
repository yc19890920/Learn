# -*- coding: utf-8 -*-

from ..conf import settings
from . import DBkit


mysqlPool = DBkit.getDBObject(
    creater='mysql', dbtype='edm_web', params=settings.DATABASES['mysql']['edm_web'], charset='UTF8', outerr=True
)

pgsqlPool = DBkit.getDBObject(
    creater='postgresql', dbtype='mail_relay', params=settings.DATABASES['postgresql']['mail_relay']
)

redis = DBkit.get_redis_connection(settings.DATABASES['redis']['redis'])
