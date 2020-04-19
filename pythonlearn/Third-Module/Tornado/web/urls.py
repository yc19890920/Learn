# -*- coding:utf-8 -*-
#

"""
the url structure of website
"""

from handlers.index import LoginHandler, LogoutHandler, UserHandler
from handlers.asynchandlers import SyncHandler, AsyncIndexHandler, AsyncIndexHandler2

URLS = [
    (r'/', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/user', UserHandler),

    (r"/sync", SyncHandler),
    (r"/async", AsyncIndexHandler)
]