- [django全文搜索学习心得（一）haystack 篇 ](https://www.cnblogs.com/chang/archive/2013/01/10/2855197.html)
- [django全文搜索学习心得（二）solr 篇 ](https://www.cnblogs.com/chang/archive/2013/01/10/2855273.html)
- [django全文搜索学习心得（三）whoosh 篇](https://www.cnblogs.com/chang/archive/2013/01/10/2855321.html)
- [实现Django的全文检索功能（二）：集成haytack](https://blog.csdn.net/wenxuansoft/article/details/8170714)
- [django全文搜索学习心得（四）sphinx篇 ](https://www.cnblogs.com/chang/archive/2013/01/10/2855355.html)
- [whoosh使用简介](https://www.cnblogs.com/chang/archive/2013/01/10/2855223.html)
- [使用Solr快速实现Django的全文搜索](https://blog.csdn.net/java2king/article/details/5422364)
- [使用Django haystack集成solr编写搜索引擎（一）](https://blog.csdn.net/sinat_33455447/article/details/59109075)
- [使用haystack实现Django的全文搜索 -- Elasticsearch搜索引擎](https://blog.csdn.net/gymaisyl/article/details/84654469)

- [WHOOSH使用手册（INDEX）（四）](https://www.cnblogs.com/mydriverc/articles/4135326.html)

## 配置
```
pip install whoosh django-haystack jieba
当然，如果你的Django项目中，使用到 REST framework，那么可以直接安装 pip install drf-haystack

# 配置Django项目的settings.py里面的INSTALLED_APPS添加Haystack
INSTALLED_APPS = [ 
        'django.contrib.admin',
        'django.contrib.auth', 
        'django.contrib.contenttypes', 
        'django.contrib.sessions', 
        'django.contrib.sites', 
 
          # Added. haystack先添加，
          'haystack', 
          # Then your usual apps... 自己的app要写在haystakc后面
          'blog',
]

# 配置引擎
# 其中顾名思义，ENGINE为使用的引擎必须要有，如果引擎是Whoosh，则PATH必须要填写，其为Whoosh 索引文件的存放文件夹。
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
```
## 创建索引
```
# 如果你想针对某个app例如mainapp做全文检索，则必须在mainapp的目录下面建立search_indexes.py文件，文件名不能修改。
import datetime
from haystack import indexes
from myapp.models import Note
 
class NoteIndex(indexes.SearchIndex, indexes.Indexable):     #类名必须为需要检索的Model_name+Index，这里需要检索Note，所以创建NoteIndex
    text = indexes.CharField(document=True, use_template=True)  #创建一个text字段
 
    author = indexes.CharField(model_attr='user')   #创建一个author字段
 
    pub_date = indexes.DateTimeField(model_attr='pub_date')  #创建一个pub_date字段
 
    def get_model(self):          #重载get_model方法，必须要有！
        return Note
 
    def index_queryset(self, using=None):   #重载index_..函数
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
        
为什么要创建索引？索引就像是一本书的目录，可以为读者提供更快速的导航与查找。
在这里也是同样的道理，当数据量非常大的时候，若要从这些数据里找出所有的满足搜索条件的几乎是不太可能的，
将会给服务器带来极大的负担。所以我们需要为指定的数据添加一个索引（目录），在这里是为Note创建一个索引，
索引的实现细节是我们不需要关心的，至于为它的哪些字段创建索引，怎么指定，正是我要给大家讲的，也是网上所不曾提到的。

每个索引里面必须有且只能有一个字段为 document=True，
这代表haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。
其他的字段只是附属的属性，方便调用，并不作为检索数据。
直到我自己完成一个搜索器，也没有用到这些附属属性，所以我索性就都删掉了，大家学习的时候也可以先注释掉不管。具体作用我也不明白，反正我没用上。

并且，haystack提供了use_template=True在text字段，这样就允许我们使用数据模板去建立搜索引擎索引的文件，
说得通俗点就是索引里面需要存放一些什么东西，例如 Note 的 title 字段，这样我们可以通过 title 内容来检索 Note 数据了，
举个例子，假如你搜索 python ，那么就可以检索出含有title含有 python 的Note了，怎么样是不是很简单？数据模板的路径为
templates/search/indexes/yourapp/note_text.txt
（推荐在项目根目录创建一个templates，并在settings.py里为其引入，使得django会从这个templates里寻找模板，当然，
只要放在任何一个你的Django能搜索到的tempaltes下面就好，关于这点我想不属于我们讨论的范畴），
templates/search/indexes/blog/note_text.txt文件名必须为要索引的类名_text.txt,其内容为
{{ object.title }}
{{ object.user.get_full_name }}
{{ object.body }}
这个数据模板的作用是对Note.title, Note.user.get_full_name,Note.body这三个字段建立索引，当检索的时候会对这三个字段做全文检索匹配。上面已经解释清楚了。
```

## 在URL配置中添加SearchView，并配置模板
```
在urls.py中配置如下url信息，当然url路由可以随意写。

(r'^search/', include('haystack.urls')),

其实haystack.urls的内容为

from django.conf.urls import url
from haystack.views import SearchView
 
urlpatterns = [
    url(r'^$', SearchView(), name='haystack_search'),
]

SearchView()视图函数默认使用的html模板路径为templates/search/search.html（再说一次推荐在根目录创建templates，并在settings.py里设置好）
所以需要在templates/search/下添加search.html文件，内容为

<h2>Search</h2>
 
    <form method="get" action=".">
        <table>
            {{ form.as_table }}
            <tr>
                <td> </td>
                <td>
                    <input type="submit" value="Search">
                </td>
            </tr>
        </table>
 
        {% if query %}
            <h3>Results</h3>
 
            {% for result in page.object_list %}
                <p>
                    <a href="{{ result.object.get_absolute_url }}">{{ result.object.title }}</a>
                    <br/>
                    {% highlight result.object.content with query css_class "highlighted" %}
                </p>
            {% empty %}
                <p>No results found.</p>
            {% endfor %}
 
            {% if page.has_previous or page.has_next %}
                <div>
                    {% if page.has_previous %}<a href="?q={{ query }}&page={{ page.previous_page_number }}">{% endif %}« Previous{% if page.has_previous %}</a>{% endif %}
                    |
                    {% if page.has_next %}<a href="?q={{ query }}&page={{ page.next_page_number }}">{% endif %}Next »{% if page.has_next %}</a>{% endif %}
                </div>
            {% endif %}
        {% else %}
            {# Show some example queries to run, maybe query syntax, something else? #}
        {% endif %}
    </form>
    
很明显，它自带了分页。
然后为大家解释一下这个文件。首先可以看到模板里使用了的变量有 form,query,page 。下面一个个的说一下。

form，很明显，它和django里的form类是差不多的，可以渲染出一个搜索的表单，相信用过Django的Form都知道，所以也不多说了，
不明白的可以去看Django文档，当然其实我倒最后也没用上，最后是自己写了个<form></form>，提供正确的参数如name="seach"，method="get"以及你的action地址就OK了。。。
如果需要用到更多的搜索功能如过滤的话可能就要自定义Form类了
（而且通过上面的例子可以看到，默认的form也是提供一个简单的过滤器的，可以供你选择哪些model是需要检索的，
如果一个都不勾的话默认全部搜索，当然我们也是可以自己利用html来模拟这个form的，所以想要实现model过滤还是很简单的，
只要模拟一下这个Form的内容就好了），
只有这样haystack才能够构造出相应的Form对象来进行检索，其实和django的Form是一样的，
Form有一个自我检查数据是否合法的功能，haystack也一样，关于这个此篇文章不做多说，因为我也不太明白（2333）。
具体细节去看文档，而且文档上关于View&Form那一节还是比较通俗易懂的，词汇量要求也不是很高，反正就连我都看懂了一些。。。

query嘛，就是我们搜索的字符串。

关于page，可以看到page有object_list属性，它是一个list，里面包含了第一页所要展示的model对象集合，那么list里面到底有多少个呢？我们想要自己控制个数怎么办呢？
不用担心，haystack为我们提供了一个接口。我们只要在settings.py里设置：
#设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE  =  8

然后关于分页的部分，大家看名字应该也能看懂吧。
如果想要知道更多的默认context带的变量，可以自己看看源码views.py里的SearchView类视图，相信都能看懂。

那么问题来了。对于一个search页面来说，我们肯定会需要用到更多自定义的 context 内容，那么这下该怎么办呢？
最初我想到的办法便是修改haystack源码，为其添加上更多的 context 内容，你们是不是也有过和我一样的想法呢？
但是这样做即笨拙又愚蠢，我们不仅需要注意各种环境，依赖关系，而且当服务器主机发生变化时，难道我们还要把 haystack 也复制过去不成？
这样太愚蠢了！突然，我想到既然我不能修改源码，难道我还不能复用源码吗？
之后，我用看了一下官方文档，正如我所想的，通过继承SeachView来实现重载 context 的内容。
官方文档提供了2个版本的SearchView，我最开始用的是新版的，最后出错了，也懒得去找错误是什么引起的了，直接使用的了旧版本的SearchView，只要你下了haystack，2个版本都是给你安装好了的。
于是我们在myapp目录下再创建一个search_views.py 文件，位置名字可以自己定，用于写自己的搜索视图，代码实例如下：

from haystack.views import SearchView
from .models import *
 
class MySeachView(SearchView):
    def extra_context(self):       #重载extra_context来添加额外的context内容
        context = super(MySeachView,self).extra_context()
        side_list = Topic.objects.filter(kind='major').order_by('add_date')[:8]
        context['side_list'] = side_list
        return context
        
然后再修改urls.py将search请求映射到MySearchView：

     url(r'^search/', search_views.MySeachView(), name='haystack_search'),
     
讲完了上下文变量，再让我们来讲一下模板标签，haystack为我们提供了 {% highlight %}和 {% more_like_this %} 2个标签，这里我只为大家详细讲解下 highlight的使用。
你是否也想让自己的检索和百度搜索一样，将匹配到的文字也高亮显示呢？ {% highlight %} 为我们提供了这个功能（当然不仅是这个标签，貌似还有一个HighLight类，这个自己看文档去吧，我英语差，看不明白）。

{% highlight <text_block> with <query> [css_class "class_name"] [html_tag "span"] [max_length 200] %}

大概意思是为 text_block 里的 query 部分添加css_class，html_tag，而max_length 为最终返回长度，相当于 cut ，
我看了一下此标签实现源码，默认的html_tag 值为 span ，css_class 值为 highlighted，max_length 值为 200，然后就可以通过CSS来添加效果。如默认时：

span.highlighted {
        color: red;
}

# 使用默认值
{% highlight result.summary with query %}
 
# 这里我们为 {{ result.summary }}里所有的 {{ query }} 指定了一个<div></div>标签，并且将class设置为highlight_me_please，这样就可以自己通过CSS为{{ query }}添加高亮效果了，怎么样，是不是很科学呢
{% highlight result.summary with query html_tag "div" css_class "highlight_me_please" %}
 
# 这里可以限制最终{{ result.summary }}被高亮处理后的长度
{% highlight result.summary with query max_length 40 %}

好了，到目前为止，如果你掌握了上面的知识的话，你已经会制作一个比较令人满意的搜索器了，接下来就是创建index文件了。
```

## 最后一步，重建索引文件
使用python manage.py rebuild_index或者使用update_index命令。

好，下面运行项目，进入该url搜索一下试试吧。
每次数据库更新后都需要更新索引，所以haystack为大家提供了一个接口，只要在settings.py里设置：
```
#自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

## 使用jieba分词
```
1 将文件whoosh_backend.py（该文件路径为python路径/lib/python2.7.5/site-packages/haystack/backends/whoosh_backend.py）拷贝到app下面，并重命名为whoosh_cn_backend.py，例如blog/whoosh_cn_backend.py。

修改为如下

from jieba.analyse import ChineseAnalyzer   #在顶部添加
 
schema_fields[field_class.index_fieldname] = TEXT(stored=True, analyzer=ChineseAnalyzer(),field_boost=field_class.boost, sortable=True)   #注意先找到这个再修改，而不是直接添加

2 在settings.py中修改引擎，如下

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'app.blog.whoosh_cn_backend.WhooshEngine',      # app.blog.whoosh_cn_backend 便是你刚刚添加的文件
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'
    },
}

3 重建索引，在进行搜索中文试试吧。
```


## highlight补充


