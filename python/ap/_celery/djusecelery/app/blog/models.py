from django.db import models

class Blog(models.Model):
    title = models.CharField("标题", unique=True, max_length=200)

    class Meta:
        db_table = 'blog'
        verbose_name = '文章'