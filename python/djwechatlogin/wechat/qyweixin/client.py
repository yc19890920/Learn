# -*-coding: utf-8 -*-
import json
import requests

class QiyeWeixinAPI(object):
    access_token_field = "access_token"
    access_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    get_user_url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo"
    get_external_userid_url = ""
    get_userinfo_url = "https://qyapi.weixin.qq.com/cgi-bin/user/get"
    openid_url = "https://qyapi.weixin.qq.com/cgi-bin/user/convert_to_openid"


    def __init__(self, corpid=None, corpsecret=None):
        self.corpid = corpid
        self.corpsecret = corpsecret

    def get_token(self):
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret,
        }
        req = requests.post(self.access_token_url, params=params)
        data = json.loads(req.text)
        return data["access_token"]

    def get_user_id(self, code, access_token):
        params = {
            'code': code,
            'access_token': access_token,
        }
        req = requests.get(self.get_user_url, params=params)
        data = json.loads(req.text)
        return data


    def get_user_info(self, access_token, user_id):
        params = {
            'userid': user_id,
            'access_token': access_token,
        }
        req = requests.get(self.get_userinfo_url, params=params)
        data = json.loads(req.text)
        return data

    def get_openid(self, access_token, user_id):
        params = {
            'access_token': access_token,
        }
        data = {
            "userid": user_id,
            'access_token': access_token,
        }
        req = requests.post(self.openid_url, data=json.dumps(data), params=params)
        data = json.loads(req.text)
        return data.get("openid")

    def get_external_userid(self, access_token, user_id):
        url = "https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list"
        params = {
             "userid": user_id,
            'access_token': access_token,
        }
        req = requests.get(url, params=params)
        data = json.loads(req.text)
        return data

