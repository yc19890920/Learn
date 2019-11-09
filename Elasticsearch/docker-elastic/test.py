# -*- coding: utf-8 -*-
import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError, NotFoundError, ConnectionError

es = Elasticsearch(hosts=[
    "http://192.168.1.24:9201/",
    "http://192.168.1.24:9202/",
    "http://192.168.1.24:9203/",
])

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res)

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res)

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
pprint.pprint(res)
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])