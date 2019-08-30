import json
import requests
from urllib.parse import urljoin

BASE_URL = 'http://192.168.1.24:6070'
AUTH = ('user1', 'abcxyz')

"""
curl -iv -H "Content-Type: application/json" -d '{"username": "user1", "password": "abcxyz"}' http://192.168.1.24:6099/api/authentication
####  {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MjgwMTY5OTl9.9WAun9_Q9eSFTWtk5GGIfNPZodrgs8NV-89cje6nsa0"}

curl -iv -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MjgwMTY5OTl9.9WAun9_Q9eSFTWtk5GGIfNPZodrgs8NV-89cje6nsa0" http://192.168.1.24:6099/api/authentication/verify
curl -iv -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MjgwMTY5OTl9.9WAun9_Q9eSFTWtk5GGIfNPZodrgs8NV-89cje6nsa0" http://192.168.1.24:6099/api/authentication/verify
"""

def get_jwt_token():
    " 获取token "
    url = urljoin(BASE_URL, '/v1/api/authentication')
    rsp = requests.post(
        url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }, data=json.dumps({ "username":"user1", "password":"abcxyz"})
    )
    print(rsp.text)
    j = rsp.json()
    return j["sanic-token"]
    return j["access_token"]

def veryfy_jwt_token(token):
    " 校验token "
    url = urljoin(BASE_URL, '/v1/api/authentication/verify')
    rsp = requests.get(
        url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token
        }
    )
    print('veryfy_jwt_token: ', rsp.ok, rsp.status_code, rsp.text)

def refresh_jwt_token(token):
    " 刷新token "
    url = urljoin(BASE_URL, '/v1/api/authentication/refresh')
    rsp = requests.get(
        url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token
        }
    )
    print('refresh_jwt_token: ', rsp.ok, rsp.status_code, rsp.text)


def get_persons(token):
    url = urljoin(BASE_URL, '/api/v1/persons')
    rsp = requests.get(
        url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token
        }
    )
    print('get_persons: ', rsp.ok, rsp.status_code, rsp.text)

def post_persons(token):
    url = urljoin(BASE_URL, '/api/v1/persons')
    json_data = {'username': '姚明', 'email': 'yaoming@hotmail.com', 'phone': '08613000001112', 'sex': 'male', "zone": "JingAn District"},
    rsp = requests.post(
        url, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token
        }, data=json.dumps(json_data),
    )
    print('post_persons: ', rsp.ok, rsp.status_code, rsp.text)

def main(token):
    veryfy_jwt_token(token)
    get_persons(token)
    post_persons(token)
    # refresh_jwt_token(token)

if __name__ == "__main__":
    import time
    source_token = get_jwt_token()
    # source_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MzE0NzM1MjV9.qPRzfChLKO3tGauk_zrBU32Q-PQDOYW7NBplMdbymzM"
    token = 'Bearer %s' % source_token
    print(token)
    main(token)