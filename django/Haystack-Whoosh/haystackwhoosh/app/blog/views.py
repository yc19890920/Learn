from django.shortcuts import render
from app.blog.models import Article

def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'blog/detail.html', {
        "article": article,
    })
