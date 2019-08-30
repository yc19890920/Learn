# coding=utf-8
import pprint
import datetime
from django.shortcuts import render
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from .weixin import WeixinAPI
from .qyweixin import QiyeWeixinAPI

@csrf_exempt
def callback(request):
    """ 回调登录
    info = {u'openid': u'oMaZnwp6MCKAxjBi0anwBsMKf3pw',
            u'access_token': u'8amyiVIWd3Ssafb08HED-8xNIB5DDDsFm6QW-bIwMaKPmFJUFA9X6X7i3rNnazqOTGNeA7jNBs8X8S-4cd9moIMZsKaT0BAFj_LjteX_Yxk',
            u'unionid': u'oh8S_wRSPZ5PfCeFnoDlPV8V1H2M', u'expires_in': 7200, u'scope': u'snsapi_login',
            u'refresh_token': u'pEbXllcSyDPMmFe4X7wmxcvmMU8A_5DfAmISaTSlYvf9cCoO6AlknluOu-2NmfdUfUMunMlrgj3bGMeR0FRctAl3mxJMUbUkJux0zl-fXu4'}
    user_info = {u'province': u'Guangdong', u'openid': u'oMaZnwp6MCKAxjBi0anwBsMKf3pw',
     u'headimgurl': u'http://wx.qlogo.cn/mmopen/PiajxSqBRaEJHPI6VNY6HmnSibI23ahh1024IYGEnYtcUxjvHDuqapdXKiacYt0lZWte9dbkVye1RJqXoDx5vI6Pw/0',
     u'language': u'zh_CN', u'city': u'Shenzhen', u'country': u'CN', u'sex': 1,
     u'unionid': u'oh8S_wRSPZ5PfCeFnoDlPV8V1H2M', u'privilege': [], u'nickname': u'\u6728\u5b50\u5a01'}
     wechat/callback?code=031OnCTU0JGrJW1239SU0GFyTU0OnCTy&state=a17c532afc204a88
     """
    # user = request.user
    code = request.GET.get('code', '')
    print "======================code=============================", code
    if not code:
        return HttpResponse('callback')

    ##################################################
    # 企业微信
    api = QiyeWeixinAPI(corpid="ww6e71658ca5a36c82", corpsecret="gUUdRsnKZZUrGEMuQxVfE0ncGvY9ICj5ndaT_OnRlbA")
    # api = QiyeWeixinAPI(corpid="ww6e71658ca5a36c82", corpsecret="Po0wQ1ThfV4Xol-_zmF_Fcn0ZDrD2pFVuD0sI7rHQJc")
    access_token = api.get_token()
    print "access_token:", access_token
    user_msg = api.get_user_id(code, access_token)
    # {u'UserId': u'YangCheng', u'DeviceId': u'', u'errmsg': u'ok', u'errcode': 0}
    print "===========user_msg==============", user_msg
    UserId = user_msg.get("UserId")
    DeviceId = user_msg.get("DeviceId") or '0'
    errmsg = user_msg.get("errmsg")
    if errmsg != "ok":
        return HttpResponse(errmsg)
    if not UserId:
        return HttpResponse(u"非企业成员")
    user_info = api.get_user_info(access_token, UserId)
    # {u'alias': u'',
    #  u'avatar': u'http://wework.qpic.cn/bizmail/NRkhsICXeofbUTKoQ7SyJj9ibIQ4cpZscEmiaWU2vEWR3uPWibMibRUfyw/0',
    #  u'department': [1],
    #  u'email': u'',
    #  u'enable': 1,
    #  u'errcode': 0,
    #  u'errmsg': u'ok',
    #  u'extattr': {u'attrs': []},
    #  u'gender': u'1',
    #  u'hide_mobile': 0,
    #  u'is_leader_in_dept': [0],
    #  u'isleader': 0,
    #  u'mobile': u'18924664854',
    #  u'name': u'\u6768\u57ce',
    #  u'order': [0],
    #  u'position': u'',
    #  u'qr_code': u'https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=vc838fdec7e68563a6',
    #  u'status': 1,
    #  u'telephone': u'',
    #  u'userid': u'YangCheng'}
    errmsg = user_info.get("errmsg")
    if errmsg != "ok":
        return HttpResponse(errmsg)
    pprint.pprint(user_info)
    openid = api.get_openid(access_token, UserId)
    print "openid:", openid
    if not openid:
        return HttpResponse(u"获取openid失败")

    data = api.get_external_userid(access_token, UserId)
    print "external_userid:", data
    response = render(request, "wx_login.html", {

    })
    expiration = (datetime.datetime.utcnow() + datetime.timedelta(hours=2))
    response.set_cookie("test",
                        "test1234",
                        expires=expiration,
                        httponly=True)
    return response
    # return HttpResponseRedirect(reverse('home'))

    ##################################################
    # 公众号
    api = WeixinAPI(appid="ww6e71658ca5a36c82", app_secret="gUUdRsnKZZUrGEMuQxVfE0ncGvY9ICj5ndaT_OnRlbA",
                    redirect_uri="http%3A%2F%2Fmail.luzi.gq%2Fweixin%2Fwechat%2Fcallback%2F")
    # auth_info = api.exchange_code_for_access_token(code=code)
    pprint.pprint(auth_info)
    print "==================================================="
    api = WeixinAPI(access_token=auth_info['access_token'])
    user_info = api.user(openid=auth_info['openid'])
    pprint.pprint(user_info)
    return HttpResponseRedirect(reverse('home'))

def home(request):
    return render(request, "home.html", context={})