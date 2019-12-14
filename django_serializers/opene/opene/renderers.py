from rest_framework import renderers
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.exceptions import ErrorDetail
# from lvt import resp_code

class resp_code:
    CODE_SUCCESS = '0000'  # 成功
    CODE_PARAM_ERROR = '0001'  # 参数错误
    CODE_NO_LOGIN = '0002'  # 没有登录
    CODE_NO_PERMISSION = '0003'  # 没有权限
    CODE_NOT_FOUND = '0004'
    #
    CODE_NEED_ENTERPRISE_AUTH = '1001'

class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, bytes):
            return str(data, encoding=self.charset)
        else:
            return data


class JSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            data = ''

        if ('status' not in data or 'msg' not in data)  and 'response' in renderer_context:
            status = renderer_context['response'].status_code
            msg = renderer_context['response'].status_text
            code = resp_code.CODE_SUCCESS
            if status == 201:
                renderer_context['response'].status_code = 200
                status = 200
                msg = 'success'
            elif status == 204:
                status = 200
                msg = 'success'
            elif status == 400:
                detail = data
                if isinstance(detail, ReturnDict) or isinstance(detail, dict):
                    for key in data:
                        detail = data[key]
                        break
                if detail and type(detail) == list:
                    detail = detail[0]
                if isinstance(detail, ErrorDetail):
                    msg = detail
                    code = detail.code
            elif status == 401:
                msg = 'No login'
                code = resp_code.CODE_NO_LOGIN
            elif status == 403:
                msg = 'No permission'
                code = resp_code.CODE_NO_PERMISSION
            elif status == 404:
                code = resp_code.CODE_NOT_FOUND

            data = {
                'status': status,
                'msg': msg,
                'data': data,
                'code': code,
            }
        return super().render(data, accepted_media_type, renderer_context)
