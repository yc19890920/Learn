# -*- coding: utf-8 -*-

# Relational DB -> Databases -> Tables -> Rows -> Columns
# Elasticsearch -> Indices   -> Types  -> Documents -> Fields
import pprint
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError, NotFoundError, ConnectionError
# es = Elasticsearch(['192.168.1.24:9200'])
# es = Elasticsearch()

es = Elasticsearch(
    hosts=[
        "http://192.168.1.24:9201/",
        "http://192.168.1.24:9202/",
        "http://192.168.1.24:9203/",
    ],
    # # turn on SSL
    # use_ssl=True,
    # # make sure we verify SSL certificates
    # verify_certs=True,
    # # provide a path to CA certs on disk
    # ca_certs='/path/to/CA_certs',
    # # PEM formatted SSL client certificate
    # client_cert='/path/to/clientcert.pem',
    # # PEM formatted SSL client key
    # client_key='/path/to/clientkey.pem'
)

#############################################################
#############################################################
# 删除索引
# result = es.indices.delete(index="news", ignore=(400, 404))
# print(result)

INDEX = "news"
DOC_TYPE = None

# 创建 Index
if es.indices.exists(index=INDEX) is not True:
    _index_mappings = {
        '_source': {
            'enabled': True
        },
        "properties": {
            "title": {
                "type": "text",
                "index": True,
                # "analyzer": "ik_max_word",
                # "search_analyzer": "ik_max_word"
            },
            "date": {
                "type": "text",
                "index": True
            },
            "url": {
                "type": "keyword",
                "index": True,
                # "index" : "not_analyzed" # 　为了避免这种问题，我们需要告诉 Elasticsearch 该字段具有精确值，要将其设置成 not_analyzed 无需分析的。
            },
        }
    }
    result = es.indices.create(index=INDEX, ignore=400)
    res = es.indices.put_mapping(index=INDEX, doc_type=DOC_TYPE, body=_index_mappings)
    print(res)


#############################################################
# 对于中文来说，我们需要安装一个分词插件，这里使用的是 elasticsearch-analysis-ik，GitHub 链接为：https://github.com/medcl/elasticsearch-analysis-ik，
# 这里我们使用 Elasticsearch 的另一个命令行工具 elasticsearch-plugin 来安装，这里安装的版本是 6.2.4，请确保和 Elasticsearch 的版本对应起来，命令如下：
# elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.7.0/elasticsearch-analysis-ik-6.7.0.zip
# 安装之后重新启动 Elasticsearch 就可以了，它会自动加载安装好的插件。
# 首先我们新建一个索引并指定需要分词的字段，代码如下：

# 先将之前的索引删除了，然后新建了一个索引，然后更新了它的 mapping 信息，
# mapping 信息中指定了分词的字段，指定了字段的类型 type 为 text，
# 分词器 analyzer 和 搜索分词器 search_analyzer 为 ik_max_word，
# 即使用我们刚才安装的中文分词插件。如果不指定的话则使用默认的英文分词器。

# 查询数据
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        },
        'url': {
            'type': 'text',
            # 'analyzer': 'ik_max_word',
            # 'search_analyzer': 'ik_max_word'
        }
    }
}
# es.indices.delete(index=INDEX, ignore=[400, 404])

# es.indices.create(index=INDEX, ignore=400)
# result = es.indices.put_mapping(index=INDEX, doc_type=DOC_TYPE, body=mapping)
# print(result)


datas = [
    {
        'title': u'美国留给伊拉克的是个烂摊子吗',
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'
    },
    {
        'title': u'公安部：各地校车将享最高路权',
        'url': 'http://www.chinanews.com/gn/2011/12-16/3536077.shtml',
        'date': '2011-12-16'
    },
    {
        'title': u'中韩渔警冲突调查：韩警平均每天扣1艘中国渔船',
        'url': 'https://news.qq.com/a/20111216/001044.htm',
        'date': '2011-12-17'
    },
    {
        'title': u'中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首',
        'url': 'http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml',
        'date': '2011-12-18'
    }
]

for data in datas:
    es.index(index=INDEX, doc_type=DOC_TYPE, body=data)

# 这里我们指定了四条数据，都带有 title、url、date 字段，然后通过 index() 方法将其插入 Elasticsearch 中，索引名称为 news，类型为 politics。
# 接下来我们根据关键词查询一下相关内容：

dsl = {
    'query': {
        'match': {
            'title': u'美国',
            # 'url': 'http://news.ifeng.com',
        }
    }
}
import json
result = es.search(index=INDEX)
pprint.pprint(result)
print "=========================================="
# print(json.dumps(result, indent=2, ensure_ascii=False))


result = es.search(index=INDEX, body=dsl)
# pprint.pprint(result)
print(json.dumps(result, indent=2, ensure_ascii=False))