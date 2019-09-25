from django.db import models
from django.utils.encoding import smart_str
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField('标题', max_length=100, null=False, blank=False, db_index=True, help_text="文章标题")
    content = models.TextField('正文', null=False, blank=False, help_text="正文内容")
    views = models.PositiveIntegerField('阅读量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    auth = models.CharField("作者", max_length=50, null=False, blank=False)
    source = models.CharField("来源", max_length=200, null=True, blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'article'
        ordering = ['-id']
        verbose_name = u'文章'

    def __str__(self):
        return smart_str(self.title)

    __repr__ = __str__

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_id': self.pk})