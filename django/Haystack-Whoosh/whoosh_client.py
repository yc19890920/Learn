import os
from whoosh.index import create_in, open_dir
from whoosh import fields
from whoosh.filedb.filestore import FileStorage
from whoosh import query, sorting
from whoosh.qparser import QueryParser, SequencePlugin
from jieba.analyse import ChineseAnalyzer

analyser = ChineseAnalyzer()    #导入中文分词工具

# 创建索引结构
WHOOSH_SCHEMA = fields.Schema(
    id=fields.ID(stored=True),
    user_id=fields.ID(stored=True),
    title=fields.TEXT(stored=True, sortable=True, analyzer=analyser),
    content=fields.TEXT(stored=True, sortable=True, analyzer=analyser),
)

def compose_whoosh_terms(field, value, schema):
    """ 合成Term """
    _qsub = QueryParser(field, schema=schema)
    _parse = _qsub.parse(value.lower())
    _terms = _parse.all_terms()
    if len(_terms) == 1:
        return query.Term(field, value.lower())
    else:
        lst = []
        for terms in _terms:
            if terms[1]:
                lst.append(
                    query.Term(field, terms[1]),
                )
        # 完整的暂时去掉
        # lst.append(query.Term(field, value.lower()))
        return query.And(lst)

def whoosh_open_idx(idx_path, schema, indexname="content"):
    storage = FileStorage(idx_path)
    ix = storage.open_index(schema=schema, indexname=indexname)
    return ix

def search(username, id=None, keyword=None, title=None, content=None, sortedby="id", orderby="desc", page=1, page_size=10):
    # 可以每个用户一个目录
    WHOOSH_PATH = '/home/python/Learn/django/Haystack-Whoosh/whoosh_index/%s' % username
    if not os.path.exists(WHOOSH_PATH):
        return []

    if not id and not keyword and not title and not content:
        return []

    filter_id = None
    if id:
        filter_id = query.Term(u"id", str(id))
    p_keyword = p_title = p_content = None
    if keyword:
        p_keyword = query.Or([
            compose_whoosh_terms('title', keyword, WHOOSH_SCHEMA),
            compose_whoosh_terms('content', keyword, WHOOSH_SCHEMA),
            # query.Term("content", keyword.lower()),
            # query.Term("subject", keyword.lower())
        ])
    if title:
        p_title = compose_whoosh_terms('title', title, WHOOSH_SCHEMA)
    if content:
        p_content = compose_whoosh_terms('content', content, WHOOSH_SCHEMA)

    lst = [i for i in [filter_id, p_keyword, p_title, p_content] if i is not None]
    if len(lst) == 1:
        q = lst[0]
    else:
        q = query.And(lst)
    print ("------------------", q)

    # 按序排列搜索结果
    if sortedby in ('id', 'title'):
        if orderby not in ("desc", "asc"):
            orderby = "desc"
        if orderby == "desc":
            facet = sorting.FieldFacet(sortedby, reverse=True)
        else:
            facet = sorting.FieldFacet(sortedby)
    else:
        facet = sorting.FieldFacet('id', reverse=True)
    print("-----------1")
    # count = 0
    rr = []
    try:
        idx = whoosh_open_idx(WHOOSH_PATH, WHOOSH_SCHEMA)
        searcher = idx.searcher()
        results = searcher.search_page(q, page, pagelen=page_size, sortedby=facet)
        # count = len(results)
        rr = [d for d in results]
    except Exception as e:
        print("-----------111", e)
    finally:
        return rr

def search2(username, id=None, keyword=None, title=None, content=None, sortedby="id", orderby="desc", page=1, page_size=10):
    # 可以每个用户一个目录
    WHOOSH_PATH = '/home/python/Learn/django/Haystack-Whoosh/whoosh_index/%s' % username
    if not os.path.exists(WHOOSH_PATH):
        return []

    # if not id and not keyword and not title and not content:
    #     return []
    index = whoosh_open_idx(WHOOSH_PATH, WHOOSH_SCHEMA)
    searcher = index.searcher()

    print("-----------2")
    parser = QueryParser("content", index.schema)
    myquery = parser.parse("分布式")
    facet = sorting.FieldFacet("id", reverse=True)  # 按序排列搜索结果
    results = searcher.search(myquery, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
    for result1 in results:
        print(dict(result1))
    print("-----------2")


def search_all(username, field_name="content", key_word="分布式", **kwargs):
    WHOOSH_PATH = '/home/python/Learn/django/Haystack-Whoosh/whoosh_index/%s' % username
    if not os.path.exists(WHOOSH_PATH):
        return []

    # if not id and not keyword and not title and not content:
    #     return []
    index = whoosh_open_idx(WHOOSH_PATH, WHOOSH_SCHEMA)
    searcher = index.searcher()

    field_name = "content"
    key_word = "分布式"

    args = {
        "limit": None,
    }
    if "sortedby" in kwargs:
        sortedby = kwargs.pop("sortedby")
        if "orderby" in kwargs:
            orderby = kwargs.pop("orderby")
        else:
            orderby = "desc"
        if orderby == "desc":
            facet = sorting.FieldFacet(sortedby, reverse=True)
        else:
            facet = sorting.FieldFacet(sortedby)
        args["sortedby"] = facet
    args.update(kwargs)
    return searcher.find(field_name, key_word, **args)

rr = search("yc", id=1, keyword=None, title=None, content=None, sortedby="id", orderby="desc", page=1, page_size=10)
print(rr)

rr = search("yc", id=None, keyword="分布式架构的前世今生", title=None, content=None, sortedby="id", orderby="desc", page=1, page_size=10)
print(rr)

rr = search("yc", id=None, keyword=None, title=None, content="分布式架构的前世今生", sortedby="id", orderby="desc", page=1, page_size=10)
print(rr)

search2("yc")

print("========================")
rr = search_all("yc")
print(rr)


def django_search(id=None, content=None, sortedby="id", orderby="desc", page=1, page_size=10):
    # 可以每个用户一个目录
    WHOOSH_PATH = '/home/python/Learn/django/Haystack-Whoosh/haystackwhoosh/haystackwhoosh/whoosh_index'
    if not os.path.exists(WHOOSH_PATH):
        return []

    if not id and not content:
        return []

    WHOOSH_SCHEMA = fields.Schema(
        id=fields.ID(stored=True),
        # user_id=fields.ID(stored=True),
        text=fields.TEXT(stored=True, sortable=True, analyzer=analyser),
        auth=fields.TEXT(stored=True, sortable=True, analyzer=analyser),
    )

    filter_id = None
    if id:
        filter_id = query.Term(u"id", str(id))
    p_content = None
    if content:
        p_content = compose_whoosh_terms('text', content, WHOOSH_SCHEMA)

    lst = [i for i in [filter_id, p_content] if i is not None]
    if len(lst) == 1:
        q = lst[0]
    else:
        q = query.And(lst)
    print ("------------------", q)

    # 按序排列搜索结果
    if sortedby in ('id', 'title'):
        if orderby not in ("desc", "asc"):
            orderby = "desc"
        if orderby == "desc":
            facet = sorting.FieldFacet(sortedby, reverse=True)
        else:
            facet = sorting.FieldFacet(sortedby)
    else:
        facet = sorting.FieldFacet('id', reverse=True)
    print("-----------1")
    # count = 0
    rr = []
    try:
        idx = whoosh_open_idx(WHOOSH_PATH, WHOOSH_SCHEMA, indexname="MAIN")
        searcher = idx.searcher()
        results = searcher.search_page(q, page, pagelen=page_size, sortedby=facet)
        # count = len(results)
        rr = [d for d in results]
    except Exception as e:
        print("-----------111", e)
    finally:
        return rr


print("=====================================")
rr = django_search(id=None, content="django", sortedby="id", orderby="desc", page=1, page_size=10)
print(rr)
