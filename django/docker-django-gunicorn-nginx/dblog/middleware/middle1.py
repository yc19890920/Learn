from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.common import CommonMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.middleware.clickjacking import XFrameOptionsMiddleware
from django.middleware.security import SecurityMiddleware
from django.middleware.http import ConditionalGetMiddleware
from django.middleware.cache import UpdateCacheMiddleware, FetchFromCacheMiddleware, CacheMiddleware
from django.middleware.locale import LocaleMiddleware
from django.middleware.gzip import GZipMiddleware
from django.core.cache import cache, caches
from django.views.decorators.vary import vary_on_headers


from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.db import connection

class Test1(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_request(self, request):
        """
        Request预处理函数：
            这个方法的调用时机在Django接收到request之后，但仍未解析URL以确定应当运行的view之前。
            Django向它传入相应的 HttpRequest 对象，以便在方法中修改。
            process_request() 应当返回 None 或 HttpResponse 对象。

        如果返回 None , Django将继续处理这个request,执行后续的中间件， 然后调用相应的view.
        如果返回 HttpResponse 对象, Django 将不再执行 任何 其它的中间件(而无视其种类)以及相应的view。 Django将立即返回该 HttpResponse .
        """
        print('Test1.process_request')
        print(request.path)
        # return HttpResponse("aaa")

    # def process_view(self, request, view, args, kwargs)
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        :param request:      	 The HttpRequest object.
        :param callback:        the Python function that Django will call to handle this request. This is the actual function object itself, not the name of the function as a string.
        :param callback_args:   将传入view的位置参数列表，但不包括request 参数(它通常是传 入view的第一个参数)
        :param callback_kwargs: 将传入view的关键字参数字典.
        :return:
        这个方法的调用时机在Django执行完request预处理函数并确定待执行的view之后，但在view函数实际执行之前。

        Just like process_request() , process_view() should return either None or an HttpResponse object.
            If it returns None , Django will continue processing this request, executing any other middleware and then the appropriate view.
            If it returns an HttpResponse object, Django won’t bother calling any other middleware (of any type) or the appropriate view. Django will immediately return that HttpResponse .
        """
        print('Test1.process_view')
        print(callback, callback_args, callback_kwargs)

    def process_response(self, request, response):
        """
        :param request:
        :param response:
        :return:

        Response后处理函数: process_response(self, request, response)

        这个方法的调用时机在Django执行view函数并生成response之后。
                Here, the processor can modify the content of a response. One obvious use case is content compression, such as gzipping of the request’s HTML.
        这个方法的参数相当直观: request 是request对象，而 response 则是从view中返回的response对象。
                request is the request object, and response is the response object returned from the view.
        不同可能返回 None 的request和view预处理函数, process_response() 必须 返回 HttpResponse 对象.
        这个response对象可以是传入函数的那一个原始对象(通常已被修改)，也可以是全新生成的。
                That response could be the original one passed into the function (possibly modified) or a brand-new one.

        """
        print('Test1.process_response')
        print(request.META['REMOTE_ADDR'])
        # print(connection.queries)
        # print(request)
        # ['COOKIES', 'DNT', 'FILES', 'GET', 'META', 'POST',
        #  '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
        #  '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
        #  '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
        #  '_encoding', '_get_post', '_get_raw_host', '_get_scheme', '_initialize_handlers', '_load_post_and_files', '_mark_post_parse_error',
        #  '_messages',  '_post_parse_error', '_read_started', '_set_post', '_stream', '_upload_handlers',
        #  'body', 'build_absolute_uri', 'close', 'content_params', 'content_type', 'encoding', 'environ', 'get_full_path', 'get_host',
        #  'get_port', 'get_raw_uri', 'get_signed_cookie', 'is_ajax', 'is_secure', 'method', 'parse_file_upload', 'path', 'path_info',
        #  'read', 'readline', 'readlines', 'resolver_match', 'scheme', 'session', 'upload_handlers', 'user', 'xreadlines']
        return response

    def process_exception(self, request, exception):
        """
        :param request:
        :param exception:
        :return:
        这个方法只有在request处理过程中出了问题并且view函数抛出了一个未捕获的异常时才会被调用。
        这个钩子可以用来发送错误通知，将现场相关信息输出到日志文件, 或者甚至尝试从错误中自动恢复。
        这个函数的参数除了一贯的 request 对象之外，还包括view函数抛出的实际的异常对象 exception 。

        process_exception() 应当返回 None 或 HttpResponse 对象.
            如果返回 None , Django将用框架内置的异常处理机制继续处理相应request。
            如果返回 HttpResponse 对象, Django 将使用该response对象，而短路框架内置的异常处理机制。
        """
        pass