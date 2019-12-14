import requests
import json
import pprint
# from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
# from opene.renderers import JSONRenderer

##########################################
# application/json
# ===================
# {'email': '1248644045@qq.com', 'name': '杨向晴', 'name2': 'aa', 'order_no': 'aa', 'province': 'aa'} <class 'dict'>
url = "http://192.168.181.135:8069/api/test/"
headers = { 'Accept': 'application/json', 'Content-Type': 'application/json' }
data = {
    'email': '1248644045@qq.com',
    'name': '杨向晴',
    'name2': 'aa',
    'order_no': 'aa',
    'province': 'aa'
}

rsp = requests.post(
    url,
    headers=headers,
    data=json.dumps(data)
)

pprint.pprint(rsp.json())

print("=============================")
##########################################
# multipart/form-data; boundary=256b4f619edf4756b8e3eec6cedb67d8
# ===================
# <QueryDict: {'email': ['1248644045@qq.com'], 'name': ['杨向晴'], 'name2': ['aa'], 'order_no': ['aa'], 'province': ['aa']}> <class 'django.http.request.QueryDict'>
url = "http://192.168.181.135:8069/api/test/"
headers = { 'Accept': 'application/json', 'Content-Type': 'multipart/form-data' }
headers = {}
data = {
    'email': '1248644045@qq.com',
    'name': '杨向晴',
    'name2': 'aa',
    'order_no': 'aa',
    'province': 'aa'
}
from requests_toolbelt.multipart.encoder import MultipartEncoder
mp_encoder = MultipartEncoder(
    fields=data
    # fields={
    #     'foo': 'bar',
    #     # plain file object, no filename or mime type produces a
    #     # Content-Disposition header with just the part name
    #     'spam': ('spam.txt', open('spam.txt', 'rb'), 'text/plain'),
    # }
)
r = requests.post(
    url,
    data=mp_encoder,  # The MultipartEncoder is posted as data, don't use files=...!
    # The MultipartEncoder provides the content-type header with the boundary:
    headers={'Accept': 'application/json', 'Content-Type': mp_encoder.content_type}
)

# rsp = requests.post(
#     url,
#     headers=headers,
#     files=data
# )

pprint.pprint(rsp.json())
