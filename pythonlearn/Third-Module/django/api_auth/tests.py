# -*- coding: utf-8 -*-

import hashlib
import time
import requests

class Client(object):

    def __init__(self):
        self.key = 'abcc7aee-7824-11e7-b733-b8aeedeaf1f5'
        self.key_name = 'auth-key'
        self.asset_api = 'http://192.168.1.24:8069/api_search/mail_status/?mail_to_list=jackson.yang,imranwel@hotmail.com@tuv.com&search_date=2017-08-04&search_hour=0state=fail_finished'


    def auth_key(self):
        """
        接口认证
        """
        ha = hashlib.md5(self.key.encode('utf-8'))      # 用self.key 做加密盐
        time_span = time.time()
        ha.update(bytes("%s|%f" % (self.key, time_span)))
        encryption = ha.hexdigest()
        result = "%s|%f" % (encryption, time_span)
        return {self.key_name: result}

    def get_asset(self):
        """
        post方式向街口提交资产信息
        """
        headers = {}
        headers.update(self.auth_key())
        r = requests.get(
            url=self.asset_api,
            headers=headers,
        )
        if r.status_code == 200:
            json_str =  r.text
            print json_str
            print type(json_str)
            import json
            j = json.loads(json_str)
            print type(j)

            import pprint
            pprint.pprint(j)
        # print r.status_code
        # print r.text


if __name__ == "__main__":
    Client().get_asset()