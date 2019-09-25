import datetime
from haystack import indexes
from app.blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):  # 类名必须为需要检索的Model_name+Index，这里需要检索Note，所以创建NoteIndex
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段
    auth = indexes.CharField(model_attr='user')  # 创建一个author字段

    def get_model(self):  # 重载get_model方法，必须要有！
        return Article

    def index_queryset(self, using=None):  # 重载index_..函数
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()