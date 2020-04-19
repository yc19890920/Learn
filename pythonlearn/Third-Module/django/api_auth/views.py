# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views import View
import time
import hashlib

ASSET_AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'     #认证的KEY
ASSET_AUTH_HEADER_NAME = 'HTTP_AUTH_KEY'        # 认证头
ASSET_AUTH_TIME = 2             # 超时时间
ENCRYPT_LIST  = []   #存放认证过的key

def api_auth(request):

    auth_key = request.META.get(ASSET_AUTH_HEADER_NAME)
    if not auth_key:        # 请求认证头不正确
        return False
    sp = auth_key.split('|')
    if len(sp) != 2:        # 格式不正确
        return False
    encrypt, timestamp = sp
    timestamp = float(timestamp)    # str换成float
    limit_timestamp = time.time() - ASSET_AUTH_TIME

    if limit_timestamp > timestamp:     # 当前程序时间与客户端时间戳对比 超时
        return False
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s|%f" % (ASSET_AUTH_KEY, timestamp), encoding='utf-8'))
    result = ha.hexdigest()
    if encrypt != result:           # md5值校验
        return False

    exist = False
    del_keys = []
    for k, v in enumerate(ENCRYPT_LIST):   # 记录当前认证，如果在过期内已经认证过，则认证失败，另过期认证记录删除
        m = v['time']
        n = v['encrypt']
        if m < limit_timestamp:
            del_keys.append(k)
            continue
        if n == encrypt:
            exist = True
    for k in del_keys:
        del ENCRYPT_LIST[k]

    if exist:
        return False
    ENCRYPT_LIST.append({'encrypt': encrypt, 'time': timestamp})
    return True


class Api(View):

    def get(self, request):
        result = api_auth(request)
        if result:
            return HttpResponse('认证成功')
        else:
            return HttpResponse('去你的吧')