#!-*- coding: utf-8 -*-
import os
import sys
import pprint
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../songci')))

from elasticsearch import Elasticsearch
from elasticsearch.transport import Transport
from elasticsearch.helpers import bulk
# from elasticsearch_dsl.connections import connections

from library.data import getPoetry

# 创建索引

class EsSongci():
    ES_HOST = [
        "http://192.168.1.24:9200/",
        "http://192.168.1.24:9201/",
    ]

    def __init__(self, index_name="songci",index_type="songci_type", hosts=None, transport_class=Transport, **kwargs):
        """
        :param index_name: 索引名称
        :param index_type: 索引类型
        :param hosts:
        :param transport_class:
        :param kwargs:
        """
        self.index_name = index_name
        self.index_type = index_type
        if hosts is None:
            self.es = Elasticsearch(hosts=self.ES_HOST, transport_class=transport_class, **kwargs)
        else:
            self.es = Elasticsearch(hosts=hosts, transport_class=transport_class, **kwargs)

    def deleteIndex(self):
        if self.es.indices.exists(index=self.index_name) is True:
            result = self.es.indices.delete(index=self.index_name, ignore=(400, 404))
            print(result)


    def createIndex(self):
        """ 创建映射：
        auth： 作者
        title： 宋体标题
        content： 词内容
        md5： _id
        创建索引,创建索引名称为songci，类型为songci_type的索引
        :param ex: Elasticsearch对象
        :return:
        """

        _index_mappings = {
            '_source': {
                'enabled': True
            },
            "properties": {
                "content": {
                    "type": "text",
                    "index": True,
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word"
                },
                # "date": {
                #     "type": "text",
                #     "index": True
                # },
                "auth": {
                    "type": "keyword",
                    "index": False,
                    # "index" : "not_analyzed" # 　为了避免这种问题，我们需要告诉 Elasticsearch 该字段具有精确值，要将其设置成 not_analyzed 无需分析的。
                },
                "title": {
                    "type": "text",
                    "index": True,
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word"
                },
                "random": {
                    "type": "integer",
                    "index": False,
                    # "index" : "not_analyzed" # 　为了避免这种问题，我们需要告诉 Elasticsearch 该字段具有精确值，要将其设置成 not_analyzed 无需分析的。
                },
            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            # res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            self.es.indices.create(index=self.index_name, ignore=400)
            res = self.es.indices.put_mapping(index='news', doc_type=self.index_type, body=_index_mappings)
            print(res)


    def builkIndexData(self):
        """  用bulk将批量数据存储到es """
        ACTIONS = []
        i = 1
        for md5, title, auth, content in getPoetry():
            # print(md5, title, auth, content)
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": md5,  #_id 也可以默认生成，不赋值
                "_source": {
                    "title": title,
                    "auth": auth,
                    "content": content,
                    "random": i,
                }
            }
            i += 1
            ACTIONS.append(action)
        success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
        print('Performed %d actions' % success)
        # print(_)

    def deleteIndexData(self, id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
        print(res)

    def updateDataByID(self, id, body=None):
        """ 更新文档 """
        # {"doc": {"age": 37, "country": "china"}}
        res = self.es.update(index=self.index_name, id=id, doc_type=self.index_type, body=body)
        print(res)


    def getDataById(self, id):
        """ 获取文档信息 """
        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
        pprint.pprint(res)
        # print(res['_source'])

        # 获取文档内容
        res = self.es.get_source(index=self.index_name, id=id, doc_type=self.index_type)
        print(res)

    def getDataByBody(self):
        """ 获取索引中的一条 """
        # doc = {'query': {'match_all': {}}}
        dsl = {
            "query": {
                "match": {
                    "auth": "吴文英111"
                }
            }
        }
        dsl1 = {
            "query": {
                "bool": {
                    "must": {"term": {"auth": "吴文英111"}}
                }
            }
        }
        dsl = {
            "query" : {
                "constant_score" : {
                    "filter" : {
                        "term" : { "random" : 2 }
                    }
                }
            }
        }
        _searched = self.es.search(index=self.index_name, body=dsl)
        pprint.pprint(_searched)
        for hit in _searched['hits']['hits']:
            pass
            # print (hit['_source']['auth'], hit['_source']['content'], hit['_source']['title'])


    def mget(self, ids):
        """
        多条数据查询
        """
        res = self.es.mget(index=self.index_name, doc_type=self.index_type, body={'ids': ids})
        pprint.pprint(res)

esci = EsSongci()
# esci.deleteIndex()
esci.createIndex()
# esci.builkIndexData()

# esci.deleteIndexData("08600192881bfb824813d11b77bc7e2e")
# esci.getDataById("75e926c0394c23015f6a9cfeae0e8ee0")

# esci.getDataByBody()

# esci.updateDataByID("75e926c0394c23015f6a9cfeae0e8ee0", {"doc": {"auth": "吴文英111"}})
# esci.updateDataByID("75e926c0394c23015f6a9cfeae0e8ee0", {"doc": {"title": "惜红衣"}})

esci.getDataByBody()

# esci.mget(["221f93fb68afe8e12181f02b5ef68cdd", "0e695ef2d55a05da40ca3d9a3aa4927e"])





