"""
https://github.com/ui/django-cached_authentication_middleware

django-cached_authentication_middleware is a drop in replacement for django.contrib.auth's built in AuthenticationMiddleware.
It tries to populate request.user by fetching user data from cache before falling back to the database.

cached_authentication_middleware是内置于AuthenticationMiddleware中的django.contrib.auth的替代品。
它尝试通过在回退到数据库之前从缓存中提取用户数据来填充request.user。

也可以AuthenticationMiddleware结合通过设置Session缓存达到一样的效果
"""

from django.conf import settings
from django.contrib.auth import get_user, SESSION_KEY
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User

CACHE_KEY = 'cached_auth_middleware:%s'
CACHE_KEY_TIMEOUT = 30


try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models import get_model


try:
    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    profile_model = get_model(app_label, model_name)
except (ValueError, AttributeError):
    profile_model = None


def profile_preprocessor(user, request):
    """ Cache user profile """
    if profile_model:
        try:
            user.get_profile()
        # Handle exception for user with no profile and AnonymousUser
        except (profile_model.DoesNotExist, AttributeError):
            pass
    return user


user_preprocessor = None
if hasattr(settings, 'CACHED_AUTH_PREPROCESSOR'):
    tmp = settings.CACHED_AUTH_PREPROCESSOR.split(".")
    module_name, function_name = ".".join(tmp[0:-1]), tmp[-1]
    func = getattr(__import__(module_name, fromlist=['']), function_name)
    if callable(func):
        user_preprocessor = func
    else:
        raise Exception("CACHED_AUTH_PREPROCESSOR must be callable with 2 arguments user and request")
else:
    user_preprocessor = profile_preprocessor


def invalidate_cache(sender, instance, **kwargs):
    if isinstance(instance, get_user_model()):
        key = CACHE_KEY % instance.id
    else:
        key = CACHE_KEY % instance.user_id
    cache.delete(key)


def get_cached_user(request):
    if not hasattr(request, '_cached_user'):
        try:
            key = CACHE_KEY % request.session[SESSION_KEY]
            # print('-----1----', key, request.session[SESSION_KEY])
            user = cache.get(key)
            # print('-----1----', user)
        except KeyError:
            user = AnonymousUser()
        if user is None:
            user = get_user(request)
            # print('-----2----', user)
            if user_preprocessor:
                user = user_preprocessor(user, request)
                # print('-----3----', user)
            cache.set(key, user, CACHE_KEY_TIMEOUT)
        request._cached_user = user
    return request._cached_user


class CachedAuthMiddleware(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super(CachedAuthMiddleware, self).__init__(*args, **kwargs)

        post_save.connect(invalidate_cache, sender=get_user_model())
        post_delete.connect(invalidate_cache, sender=get_user_model())
        if profile_model:
            post_save.connect(invalidate_cache, sender=profile_model)
            post_delete.connect(invalidate_cache, sender=profile_model)

    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        request.user = SimpleLazyObject(lambda: get_cached_user(request))