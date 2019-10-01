# Relational DB -> Databases -> Tables -> Rows -> Columns
# Elasticsearch -> Indices   -> Types  -> Documents -> Fields
import pprint
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError, NotFoundError, ConnectionError
# es = Elasticsearch(['192.168.1.24:9200'])
# es = Elasticsearch()

es = Elasticsearch(
    hosts=[
        "http://192.168.1.24:9200/",
        "http://192.168.1.24:9201/",
        # "http://192.168.1.24:9202/",

        # "http://localhost:9200/",
        # "http://localhost:9201/",
        # "http://localhost:9202/",
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
# 创建 Index
# result = es.indices.create(index='news', ignore=400)
# print(result)
# {'acknowledged': True, 'shards_acknowledged': True, 'index': 'news'}
# {'error': {'root_cause': [{'type': 'resource_already_exists_exception', 'reason': 'index [news/QM6yz2W8QE-bflKhc5oThw] already exists', 'index_uuid': 'QM6yz2W8QE-bflKhc5oThw', 'index': 'news'}], 'type': 'resource_already_exists_exception', 'reason': 'index [news/QM6yz2W8QE-bflKhc5oThw] already exists', 'index_uuid': 'QM6yz2W8QE-bflKhc5oThw', 'index': 'news'}, 'status': 400}

#############################################################
# 删除索引
# result = es.indices.delete(index="news", ignore=(400, 404))
# print(result)

#############################################################
# 插入数据
data1 = {
    'title': "美国留给伊拉克是一个烂摊子吗？",
    'url':  "http://view.news.qq.com/zt2011/usa_iraq/index.htm",
}
data2 = {
    'title': "Python和Elasticsearch 构建简易搜索",
    'url':  "https://bainingchao.github.io/2019/05/24/Python-%E5%92%8C-Elasticsearch-%E6%9E%84%E5%BB%BA%E7%AE%80%E6%98%93%E6%90%9C%E7%B4%A2/",
}
data3 = {
    'title': "一文了解 Elasticsearch 及其与 Python 的对接实现",
    'url':  "https://juejin.im/post/5bad93efe51d450e9d64aede",
}
# 这里我们首先声明了一条新闻数据，包括标题和链接，然后通过调用 create() 方法插入了这条数据，在调用 create() 方法时，
# 我们传入了四个参数，index 参数代表了索引名称，doc_type 代表了文档类型，body 则代表了文档具体内容，id 则是数据的唯一标识 ID。
# 结果中 result 字段为 created，代表该数据插入成功。


# result = es.create(index='news', doc_type="politics", id=1, body=data1)
# print(result)
# {'_index': 'news', '_type': 'politics', '_id': '1', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}

# result = es.create(index='news', doc_type="politics", id=2, body=data2)
# print(result)
# {'_index': 'news', '_type': 'politics', '_id': '1', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}

# 另外其实我们也可以使用 index() 方法来插入数据，但与 create() 不同的是，create() 方法需要我们指定 id 字段来唯一标识该条数据，而 index() 方法则不需要，如果不指定 id，会自动生成一个 id，调用 index() 方法的写法如下：
# result = es.index(index='news', body=data3, doc_type='politics')
# print(result)
# {'_index': 'news', '_type': 'politics', '_id': 'ERZqgW0BeTO9ZBlvNRX_', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}


#############################################################
# 更新数据
# 更新数据也非常简单，我们同样需要指定数据的 id 和内容，调用 update() 方法即可，代码如下：
data = {
    "doc": {
        "title": "美国留给伊拉克的是个烂摊子吗？",
        'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm',
        'date': '2011-12-16'
    }
}
# result = es.update(index='news', id=1, doc_type='politics', body=data)
# print(result)


#############################################################
# 查询数据
mapping = {
    'properties': {
        'title': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        }
    }
}
# es.indices.delete(index='news', ignore=[400, 404])
# es.indices.create(index='news', ignore=400)
# result = es.indices.put_mapping(index='news', doc_type='politics', body=mapping)
# print(result)


result = es.search(index='news', body=None)
print(result)
pprint.pprint(result)

