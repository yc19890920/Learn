
from django.utils.deprecation import MiddlewareMixin

class Test2(MiddlewareMixin):

    def process_request(self, request):
        print('Test2.process_request')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('Test2.process_view')

    def process_response(self, request, response):
        print('Test2.process_response')
        return response