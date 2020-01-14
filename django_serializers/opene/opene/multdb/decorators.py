"""
扩展了 django_replicated 方式，支持django rest 增加装饰器（支持函数、rest视图），控制主备使用。
其他设置还是参考 django_replicated 进行设置即可。
参考链接：  https://github.com/yandex/django_replicated
"""
from functools import wraps
from django.utils.decorators import method_decorator
from django_replicated.utils import Routers
from django_replicated.decorators import use_master, use_slave

def rest_use_database(router):
    def func_wrapper(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            routers = Routers()
            routers.init(router)
            try:
                return view_func(*args, **kwargs)
            finally:
                routers.reset()
        return wrapped_view
    return func_wrapper


# rest_use_master = rest_use_database("master")
# rest_use_slave = rest_use_database("slave")

# 装饰器使用
use_master = method_decorator(use_master)
use_slave = method_decorator(use_slave)


