# -*- coding: utf-8 -*-

import json
import hashlib
import requests
import datetime

WEB_API_HOST = '127.0.0.1'
WEB_API_PORT = 5000
WEB_API_AUTH_KEY = 'oDerVOA0Dfh6qAk5J'

url = 'http://{host}:{port}/api'.format(**{
    'host': WEB_API_HOST,
    'port': WEB_API_PORT,
})

data = {
    'action':  'public-handle',
    'auth': hashlib.md5('%s-%s' % (WEB_API_AUTH_KEY, datetime.datetime.now().strftime("%Y%m%d"))).hexdigest(),
}

try:
    r = requests.get(url, data)
    print dir(r)
except BaseException as e:
    print e

print '-------------------------'

url = u'http://{host}:{port}/api'.format(**{
    'host': WEB_API_HOST,
    'port': WEB_API_PORT,
})

data = {
    'auth': hashlib.md5('%s-%s' % (WEB_API_AUTH_KEY, datetime.datetime.now().strftime("%Y%m%d"))).hexdigest(),
    'action': 'update-customer',
    'user_id': 2369,
    'address': u'深圳宝安'
}

try:
    r = requests.get(url, data)
    print dir(r)
except BaseException as e:
    print e
