from django.utils.deprecation import MiddlewareMixin

from django.http import HttpResponseRedirect
from django.urls import reverse

class MyLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'user' not in request.session or not request.session['user']:
            return HttpResponseRedirect(reverse("login")) #本网站内部跳转仅需要相对路径
            # return HttpResponseRedirect("http://www.baidu.com")  #跳到外部网站需要加http的完整路径