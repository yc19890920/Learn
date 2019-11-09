# -*- coding: utf-8 -*-
"""
查看数据：
http://192.168.1.24:9201/share/email/_search

查看映射：
我们可以使用_mapping后缀来查看Elasticsearch中的映射。
在本章开始我们已经找到索引share类型email中的映射：
http://192.168.1.24:9201/share/_mapping/email
"""
import json
import pprint
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError, NotFoundError, ConnectionError

es = Elasticsearch(hosts=[
    "http://192.168.1.24:9201/",
    "http://192.168.1.24:9202/",
    "http://192.168.1.24:9203/",
])

INDEX = "share"
DOC_TYPE = "email"
INDEX_MAPPING = {
    '_source': { 'enabled': True },
    "properties": {
        # 邮箱ID
        "email": { "type": "long" },
        # 活跃度ID 列表
        "activity": {"type": "integer"},
        # 行业ID 列表
        "industry": { "type": "integer" },
        # 地区ID 列表
        "area": { "type": "integer" },
        # 详细信息ID 列表
        "detailed": { "type": "integer" },
        # 所属域名列表
        #  @qq.com @vip.qq.com @foxmail.com @126.com @163.com @vip.163.com @sohu.com @gov.gov.com .org @live.cn @sina.com @hotmail.com @gmail.com @outlook.com
        # [
        #     (0, u"其他"), (1, "qq.com"), (2, "vip.qq.com"), (3, "foxmail.com"), (4, "126.com"),
        #     (5, "163.com"), (6, "vip.163.com"), (7, "sohu.com"), (8, "gov.gov.com"),
        #     (9, "live.cn"), (10, "sina.com"), (11, "hotmail.com"), (12, "gmail.com"), (13, "outlook.com"), (14, ".org")
        # ]
        "domain": { "type": "integer" },
    }
}

# es.indices.delete(index=INDEX, ignore=[400, 404])
# 创建索引
if es.indices.exists(index=INDEX) is not True:
    result = es.indices.create(index=INDEX, ignore=400)
    result = es.indices.put_mapping(index=INDEX, doc_type=DOC_TYPE, body=INDEX_MAPPING)
    # print "======================INDEX_MAPPING====================="
    print(result)


# assert 1==2

datas = [
    {
        'email': 1,
        'activity': [1, 2],
        'industry': [11, 22],
        'area': [111, 222],
        'detailed': [1111, 2222],
        'domain': 1,
    },
    {
        'email': 2,
        'activity': [3, 4],
        'industry': [12, 23],
        'area': [112, 223],
        'detailed': [1112, 2223],
        'domain': 1,
    },
    {
        'email': 3,
        'activity': [2, 5],
        'industry': [11, 22],
        'area': [111, 222],
        'detailed': [1112, 2222],
        'domain': 1,
    },
    {
        'email': 4,
        'activity': [2, 8],
        'industry': [11, 22],
        'area': [111, 222],
        'detailed': [11711, 22822],
        'domain': 1,
    },
    {
        'email': 5,
        'activity': [3, 9],
        'industry': [11, 22],
        'area': [111, 222],
        'detailed': [111511, 222262],
        'domain': 1,
    },
    {
        'email': 6,
        'activity': [11, 10],
        'industry': [11, 22],
        'area': [111, 222],
        'detailed': [11121, 22322],
        'domain': 1,
    },
    {
        'email': 7,
        'activity': [7, 8],
        'industry': [11, 22],
        'area': [111, 222],
        'detailed': [11111, 22222],
        'domain': 1,
    },
]

# for data in datas:
#     es.index(index=INDEX, doc_type=DOC_TYPE, body=data, id=data["email"])

print "=====================dsl1====================="
# 查询邮箱等于1 的数据
dsl = {
    "query": {
        "term" : {
            "email" : 1
        }
    },
    "sort": {
        "_id": {
            "order": "desc" # 降序
        }
    }
}
result = es.search(index=INDEX, body=dsl)
pprint.pprint(result)

print "=====================dsl2====================="
# 查询活跃度等于1 或者等于5 的数据
dsl = {
    "query": {
        "terms": {
            "activity": [1, 5]
        }
    },
    "sort": {
        "_id": {
            "order": "desc" # 降序
        }
    }
}
result = es.search(index=INDEX, body=dsl)
pprint.pprint(result)

print "=====================dsl3====================="
# 查询活跃度等于5 的数据
dsl = {
    "query": {
        "term": {
            "activity": 5
        }
    },
    "sort": {
        "_id": {
            "order": "desc" # 降序
        }
    }
}
result = es.search(index=INDEX, body=dsl)
pprint.pprint(result)


print "======================all===================="
dsl = {
    "query": {
        "match_all": {}
    },
    "size": 1,
    "from": 0,
}
result = es.search(index=INDEX, body=dsl)
pprint.pprint(result)

print "=====================dsl4====================="
# 查询活跃度等于5 的数据
dsl = {
    "_source": ["email"],
    "query" : {
        "bool" : {
            "must" :  [
                { "terms" : {"activity" : [2,8]}},
                { "terms" : {"detailed" : [11111, 11711]}}
            ],
            "must_not" : {"terms" : {"domain" : [2,3]} }
        }
    },
    "sort": {
        "_id": {
            "order": "desc" # 降序
        }
    }
}
result = es.search(index=INDEX, body=dsl)
pprint.pprint(result)
