# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.cache import cache_page
from django.db.models import Q, F

from app.blog.models import Tag, Category, Article, BlogComment, Suggest
from app.blog.forms import SuggestForm, BlogCommentForm
from app.blog import tools as cache
from libs.tools import getClientIP
from app.blog.tasks import celery_send_email, views_article
from django.views.decorators.cache import cache_page

import logging
logger = logging.getLogger(__name__)

# @cache_page(1800, key_prefix="dblog:pages:index")
def index(request):
    article_list = Article.objects.filter(status='p')

    tag_list = cache.getTaglist()
    hot_list = cache.getHotlist()
    newart_list = cache.getNewArticlelist()
    newcom_list = cache.getNewCommontlist()
    return render(request, 'blogview/index.html', {
        "article_list": article_list,

        "tag_list": tag_list,
        "hot_list": hot_list,
        "newart_list": newart_list,
        "newcom_list": newcom_list,
    })

def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    form = BlogCommentForm(article)
    if request.method == "POST":
        form = BlogCommentForm(article, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'评论成功，谢谢！')
            current_uri = "{}#list-talk".format( reverse( "detail", args=(article_id,) ) )
            return HttpResponseRedirect(current_uri)
            # return redirect("detail", article_id=article_id)

    tag_list = cache.getTaglist()
    hot_list = cache.getHotlist()
    newart_list = cache.getNewArticlelist()

    # 相关文章
    refer_list = Article.objects.filter(status='p', id__in=article.get_refer_ids).exclude(id=article_id)
    ip = getClientIP(request)

    views_article.delay(ip, article_id)
    # if cache.shouldIncrViews(ip, article_id):
    #     article.views = F("views") +1
    #     article.save()
    return render(request, 'blogview/detail.html', {
        "form": form,
        "article": article,
        "refer_list": refer_list,

        "tag_list": tag_list,
        "hot_list": hot_list,
        "newart_list": newart_list,
    })

def score(request):
    if request.method == "POST":
        art_id = request.POST.get("poid", "0")
        obj = get_object_or_404(Article, pk=art_id)
        obj.likes = F("likes") + 1
        obj.save()
    return HttpResponse(json.dumps({'status': "ok"}), content_type="application/json")

# @cache_page(1800, key_prefix="dblog:pages:tag")
def tag(request, tag_id):
    tag_obj = get_object_or_404(Tag, pk=tag_id)
    article_list = Article.objects.filter(tags=tag_id, status='p')

    tag_list = cache.getTaglist()
    hot_list = cache.getHotlist()
    newart_list = cache.getNewArticlelist()
    newcom_list = cache.getNewCommontlist()
    return render(request, 'blogview/index.html', {
        "tag_name": tag_obj,
        "article_list": article_list,
        "article_index_limit_tag": True,

        "tag_list": tag_list,
        "hot_list": hot_list,
        "newart_list": newart_list,
        "newcom_list": newcom_list,
    })

def search(request):
    search_for = request.GET['search_for']
    if search_for:
        article_list = Article.objects.filter(title__icontains=search_for)

        tag_list = cache.getTaglist()
        hot_list = cache.getHotlist()
        newart_list = cache.getNewArticlelist()
        newcom_list = cache.getNewCommontlist()
        return render(request, 'blogview/index.html', {
            "search_for": search_for,
            "article_list": article_list,

            "tag_list": tag_list,
            "hot_list": hot_list,
            "newart_list": newart_list,
            "newcom_list": newcom_list,
        })
    else:
        return redirect('index')

# @cache_page(60*60)
def about(request):
    form = SuggestForm()
    if request.method == "POST":
        form = SuggestForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                # 使用celery并发处理邮件发送的任务
                celery_send_email.delay(u'访客意见', form.cleaned_data['content'])
            except Exception as e:
                logger.error(u"邮件发送失败: {}".format(e))
            messages.add_message(request, messages.SUCCESS, u'您宝贵的意见已收到，谢谢！')
            return redirect("about")
    return render(request, 'blogview/about.html', {
        "form": form,
    })