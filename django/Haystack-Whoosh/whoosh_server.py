"""
/home/python/pyenv/versions/haystack/bin/python whoosh_client.py

Whoosh 有一些很有用的预定义 field types，你也可以很easy的创建你自己的。
whoosh.fields.ID
这个类型简单地将field的值索引为一个独立单元（这意味着，他不被分成单独的单词）。这对于文件路径、URL、时间、类别等field很有益处。
whoosh.fields.STORED
这个类型和文档存储在一起，但没有被索引。这个field type不可搜索。这对于你想在搜索结果中展示给用户的文档信息很有用。
whoosh.fields.KEYWORD
这个类型针对于空格或逗号间隔的关键词设计。可索引可搜索（部分存储）。为减少空间，不支持短语搜索。
whoosh.fields.TEXT
这个类型针对文档主体。存储文本及term的位置以允许短语搜索。
whoosh.fields.NUMERIC
这个类型专为数字设计，你可以存储整数或浮点数。
whoosh.fields.BOOLEAN
这个类型存储bool型
whoosh.fields.DATETIME
这个类型为 datetime object而设计（更多详细信息）
whoosh.fields.NGRAM  和 whoosh.fields.NGRAMWORDS
"""

import os
import errno
from whoosh.index import create_in, open_dir
from whoosh import fields
from whoosh.filedb.filestore import FileStorage
from whoosh import query, sorting
from whoosh.index import EmptyIndexError,LockError

from jieba.analyse import ChineseAnalyzer

analyser = ChineseAnalyzer()    #导入中文分词工具

def create_dir(_dir):
    if not os.path.exists(_dir):
        try:
            os.makedirs(_dir, 0o744)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise EnvironmentError(
                    "Cache directory '%s' does not exist "
                    "and could not be created'" % _dir)

def whoosh_writter(index):
    """ 判断文件是不是加锁了"""
    while True:
        try:
            writter = index.writer()
            return writter
            writter.cancel()
        except LockError:
            pass

def server(username):
    # 可以每个用户一个目录
    WHOOSH_PATH = '/home/python/Learn/django/Haystack-Whoosh/whoosh_index/%s' % username

    # 创建索引结构
    WHOOSH_SCHEMA = fields.Schema(
        id=fields.ID(stored=True),
        user_id=fields.ID(stored=True),
        title=fields.TEXT(stored=True, sortable=True, analyzer=analyser),
        content=fields.TEXT(stored=True, sortable=True, analyzer=analyser),
    )

    if not os.path.exists(WHOOSH_PATH):
        # os.mkdir(WHOOSH_PATH)
        create_dir(WHOOSH_PATH)
        ix = create_in(WHOOSH_PATH, schema=WHOOSH_SCHEMA, indexname='content')  # path 为索引创建的地址，indexname 为索引名称

    ix = open_dir(WHOOSH_PATH, indexname='content')

    # writter = ix.writer()
    writter = whoosh_writter(ix)
    writter.add_document(id=str(1), user_id="1", title='分布式架构的前世今生...',content= '随着社会的发展，技术的进步，以前的大型机架构很显然由于高成本、难维护等原因渐渐地变得不再那么主流了，'
                                                                               '替代它的就是当下最火的分布式架构，从大型机到分布式，经历了好几个阶段，我们弄明白各个阶段的架构，才能更好地理解和体会分布式架构的好处，'
                                                                               '那么本文我们就来聊聊分布式架构的演进过程，希望能给大家带来眼前一亮的感觉。')
    writter.add_document(id=str(2), user_id="1", title='高并发的核心技术-幂等的实现方案',content= '我们发起一笔付款请求，应该只扣用户账户一次钱，当遇到网络重发或系统bug重发，也应该只扣一次钱；')
    writter.commit()
    # writter.cancel()

server("yc")