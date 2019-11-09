# -*- coding: utf-8 -*-
"""
查看数据：
http://192.168.1.24:9201/db/table/_search
"""

import pprint
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch(hosts=[
    "http://192.168.1.24:9201/",
    "http://192.168.1.24:9202/",
    "http://192.168.1.24:9200/",
])
INDEX = "db"
DOC_TYPE = "table"

def delete_index():
    if es.indices.exists(index=INDEX) is True:
        es.indices.delete(index=INDEX, ignore=[400, 404])

def create_index():
    # 索引是否存在
    if es.indices.exists(index=INDEX) is not True:
        INDEX_MAPPING = {
            '_source': { 'enabled': True },
            "properties": {
                # 邮箱
                "email": { "type": "keyword", "index": True},
                # 属性ID 列表
                "attrs": {"type": "long"},
            }
        }
        result = es.indices.create(index=INDEX, ignore=400)
        print(result)
        result = es.indices.put_mapping(index=INDEX, doc_type=DOC_TYPE, body=INDEX_MAPPING)
        print(result)

def create_data():
    """ 比较各种操作 对操作一条数据的创建更新操作，是否都影响，
    结论：影响的结构都一样，则可直接使用创建操作。
    """
    # 创建
    data = {"email": "1248644045@qq.com", "attrs": [1,2]}
    result = es.index(index=INDEX, doc_type=DOC_TYPE, body=data, id=1)
    print(u"==================== 创建 ====================")
    print(result)
    # {u'_type': u'table', u'_seq_no': 0, u'_shards': {u'successful': 2, u'failed': 0, u'total': 2}, u'_index': u'db', u'_version': 1, u'_primary_term': 1, u'result': u'created', u'_id': u'1'}

    # 覆盖创建
    data = {"email": "1248644045@qq.com", "attrs": [1,2,3]}
    result = es.index(index=INDEX, doc_type=DOC_TYPE, body=data, id=1)
    print(u"==================== 覆盖创建 ====================")
    print(result)
    # {u'_type': u'table', u'_seq_no': 2, u'_shards': {u'successful': 2, u'failed': 0, u'total': 2}, u'_index': u'db', u'_version': 3, u'_primary_term': 1, u'result': u'updated', u'_id': u'1'}

    # # 批量添加
    actions = [
        {"_index": INDEX, "_type": DOC_TYPE, "_id": 1, "_source": {"email": "1248644045@qq.com", "attrs": [1,2,3,4] } },
        {"_index": INDEX, "_type": DOC_TYPE, "_id": 2, "_source": {"email": "1248644045@qq.comr", "attrs": [4, 5, 6]}},
        {"_index": INDEX, "_type": DOC_TYPE, "_id": 3, "_source": {"email": "378704992@qq.com", "attrs": [3, 9]}},
        {"_index": INDEX, "_type": DOC_TYPE, "_id": 4, "_source": {"email": "1248644045@163.com", "attrs": [2, 3]}},
    ]
    success, result = bulk(es, actions, index=INDEX, raise_on_error=True)
    print(u"==================== 批量添加 ====================")
    print('Performed %d actions' % success)
    print(result)

    # 更新
    data = {"doc": {"email": "1248644045@qq.com", "attrs": [1,2,3,4,5]}}
    result = es.update(index=INDEX, id=1, doc_type=DOC_TYPE, body=data)
    print(u"==================== 更新 ====================")
    print(result)
    # {u'_type': u'table', u'_seq_no': 15, u'_shards': {u'successful': 2, u'failed': 0, u'total': 2}, u'_index': u'db', u'_version': 16, u'_primary_term': 1, u'result': u'updated', u'_id': u'1'}


def search_data():
    """
    各种条件的查询:
    """
    # 获取文档内容
    result = es.get_source(index=INDEX, id=1, doc_type=DOC_TYPE)
    print(u"==================== 获取 id=1 文档内容 ====================")
    print(result)
    # {u'email': u'1248644045@qq.com', u'attrs': [1, 2, 3, 4, 5]}

    # 获取文档内容
    result = es.get(index=INDEX, id=1, doc_type=DOC_TYPE)
    print(u"==================== 获取 id=1 文档信息 ====================")
    print(result)
    # {u'_type': u'table', u'_seq_no': 27, u'_index': u'db', u'_source': {u'email': u'1248644045@qq.com', u'attrs': [1, 2, 3, 4, 5]}, u'_version': 28, u'_primary_term': 1, u'found': True, u'_id': u'1'}

    # # 等于查询 term与terms, 查询 name='tom cat' 这个值不会分词必须完全包含
    # res = es.search(index='test6', size=20, body={
    #     "query": {
    #         "term": {
    #             "name": "tom cat"
    #         }
    #     }
    # })

    # 等于查询 term与terms, 查询 email='1248644045@qq.com' 或 email='378704992@qq.com'
    result = es.search(index=INDEX, size=20, body={
        "query": {
            "terms": {
                "email": ["1248644045@qq.com", "378704992@qq.com"]
            }
        }
    })
    # 映射的时候必须创建 type = keyword 才能使用此查询条件
    print(u"==================== 等于查询 term与terms, 查询 email='1248644045@qq.com' 或 email='378704992@qq.com' ====================")
    print(result)
    """
    {u'hits': {u'hits': [{u'_score': 1.0, u'_type': u'table', u'_id': u'1',
                          u'_source': {u'email': u'1248644045@qq.com', u'attrs': [1, 2, 3, 4]}, u'_index': u'db'},
                         {u'_score': 1.0, u'_type': u'table', u'_id': u'3',
                          u'_source': {u'email': u'378704992@qq.com', u'attrs': [3, 9]}, u'_index': u'db'}],
               u'total': 2, u'max_score': 1.0},
     u'_shards': {u'successful': 5, u'failed': 0, u'skipped': 0, u'total': 5}, u'took': 16, u'timed_out': False}
     """

    # ids , 查询id 1, 2的数据 相当于mysql的 in
    result = es.search(index=INDEX, size=20, body={
        "query": {
            "ids": {
                "values": ["1", "2"]
            }
        }
    })
    print(u"==================== ids , 查询id 1, 2的数据 相当于mysql的 in ====================")
    print(result)
    """
    {u'hits': {u'hits': [{u'_score': 1.0, u'_type': u'table', u'_id': u'2',
                          u'_source': {u'email': u'1248644045@qq.comr', u'attrs': [4, 5, 6]}, u'_index': u'db'},
                         {u'_score': 1.0, u'_type': u'table', u'_id': u'1',
                          u'_source': {u'email': u'1248644045@qq.com', u'attrs': [1, 2, 3, 4, 5]}, u'_index': u'db'}],
               u'total': 2, u'max_score': 1.0},
     u'_shards': {u'successful': 5, u'failed': 0, u'skipped': 0, u'total': 5}, u'took': 17, u'timed_out': False}
     """

    # 复合查询bool , bool有3类查询关系，must(都满足),should(其中一个满足),must_not(都不满足)
    # 查询 email='1248644045@qq.com' 或 email='378704992@qq.com' 并且 attrs 属性为 1 或者9， 并且 attrs 不能为 2, 4
    result = es.search(index=INDEX, size=20, body={
        # "_source": ["email"], # 搜索结果只包含哪些字段
        "query": {
            "bool": {
                "must" :  [
                    { "terms" : {"email" : ["1248644045@qq.com", "378704992@qq.com"]}},
                    { "terms" : {"attrs" : [9, 1]}}
                ],
                "must_not" : {"terms" : {"attrs" : [2, 4]} }
            }
        },
        "from": 0,  # 从第一条数据开始
        "size": 5,  # 获取5条数据
        "sort": { # 排序
            "_id": {
                "order": "desc"  # 降序
            }
        }
    })
    print(u"==================== 查询 email='1248644045@qq.com' 或 email='378704992@qq.com' 并且 attrs 属性为 1 或者9， 并且 attrs 不能为 2, 4 ====================")
    print(result)
    """
    {u'hits': {u'hits': [{u'_score': 2.0, u'_type': u'table', u'_id': u'3',
                          u'_source': {u'email': u'378704992@qq.com', u'attrs': [3, 9]}, u'_index': u'db'}],
               u'total': 1, u'max_score': 2.0},
     u'_shards': {u'successful': 5, u'failed': 0, u'skipped': 0, u'total': 5}, u'took': 8, u'timed_out': False}
     """

    # 查询所有数据
    # 方法1
    result1 = es.search(index=INDEX, size=20)
    # 方法2
    result2 = es.search(index=INDEX, body={
        "query": {
            "match_all": {}
        },
        "from": 1,  # 从第二条数据开始， 即_id=3,2 两条数据， _id=4并不能获取
        "size": 2,  # 获取2条数据
        "sort": { # 排序
            "_id": {
                "order": "desc"  # 降序
            }
        }
    })
    print(u"==================== 查询所有数据 ====================")
    print(result1)
    print(result2)
    """
    {u'hits': {u'hits': [{u'_score': 1.0, u'_type': u'table', u'_id': u'2',
                          u'_source': {u'email': u'1248644045@qq.comr', u'attrs': [4, 5, 6]}, u'_index': u'db'},
                         {u'_score': 1.0, u'_type': u'table', u'_id': u'4',
                          u'_source': {u'email': u'1248644045@163.com', u'attrs': [2, 3]}, u'_index': u'db'},
                         {u'_score': 1.0, u'_type': u'table', u'_id': u'1',
                          u'_source': {u'email': u'1248644045@qq.com', u'attrs': [1, 2, 3, 4, 5]}, u'_index': u'db'},
                         {u'_score': 1.0, u'_type': u'table', u'_id': u'3',
                          u'_source': {u'email': u'378704992@qq.com', u'attrs': [3, 9]}, u'_index': u'db'}],
               u'total': 4, u'max_score': 1.0},
     u'_shards': {u'successful': 5, u'failed': 0, u'skipped': 0, u'total': 5}, u'took': 3, u'timed_out': False}
     """

if __name__ == "__main__":
    # delete_index()

    create_index()

    create_data()

    search_data()