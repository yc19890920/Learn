# -*- coding: utf-8 -*-
#

import requests


import json
import requests
from urlparse import urljoin

BASE_URL = 'http://192.168.1.24:8080'
AUTH = ('admin', '1qaz@WSX')


def get_tag_list():
    url = urljoin(BASE_URL, '/rest/tag/')
    url = "http://192.168.1.24:8080/rest/tag/?limit=10&offset=10"
    rsp = requests.get(
        url, auth=AUTH, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    # assert rsp.ok
    print rsp.status_code
    print rsp.text


def post_tag():
    json_data = dict(
        name='Test',
    )
    rsp = requests.post(
        urljoin(BASE_URL, '/rest/tag/'), auth=AUTH, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }, data=json.dumps(json_data))
    print rsp.status_code
    print rsp.json()


def get_tag():
    rsp = requests.get(
        urljoin(BASE_URL, '/rest/tag/15/'), auth=AUTH, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    print rsp.ok, rsp.status_code
    print rsp.json()
    # assert rsp.ok


def put_tag():
    json_data = dict(
        name='TTT',
    )
    # 注意最后的 /
    rsp = requests.put(
        urljoin(BASE_URL, '/rest/tag/15/'), auth=AUTH, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }, data=json.dumps(json_data),
    )
    print rsp.ok, rsp.status_code
    # assert rsp.ok, rsp.status_code


def patch_tag():
    json_data = dict(
        name='TTT2',
    )
    rsp = requests.patch(
        urljoin(BASE_URL, '/rest/tag/15/'), auth=AUTH, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }, data=json.dumps(json_data),
    )
    print rsp.ok, rsp.status_code
    # assert rsp.ok, rsp.status_code

def main():
    # get_tag_list()
    post_tag()
    # get_tag()
    # put_tag()
    # patch_user()


if __name__ == "__main__":
    main()