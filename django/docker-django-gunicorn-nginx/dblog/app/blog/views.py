# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import os
import json
import uuid
import random
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import query, Q
from django.conf import settings
from django.utils.encoding import smart_str
from app.blog.models import Tag, Category, Article, BlogComment, Suggest, CKeditorPictureFile, ArticleTags
from app.blog.forms import ArticleForm, TagForm, CategoryForm, ShowForm, AdminLogForm
from django.utils.translation import ugettext_lazy as _
from auditlog.models import LogEntry


#########################################
# 管理员操作日志
@login_required
def admin_log(request):
    form = AdminLogForm(request.GET)
    return render(request, "blog/admin_log.html", context={
        "form": form,
    })

@login_required
def admin_log_ajax(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    content_type = data.get('content_type', '')
    domain_id = data.get('domain', '')
    logs = LogEntry.objects.all()
    if content_type:
        try:
            content_type_id = int(content_type)
            logs = logs.filter(content_type_id=content_type_id)
        except BaseException as e:
            logs = logs.filter(extend_type=content_type)
    
    if start_time:
        logs = logs.filter(timestamp__gte=start_time)
    if end_time:
        logs = logs.filter(timestamp__lte=start_time)
    if search:
        logs = logs.filter(remote_addr__icontains=search)
        # Q(remote_addr__icontains=search) | Q(changes__icontains=search) )
    
    colums = ['id', 'content_type', 'changes', 'action', 'actor', 'remote_addr', 'timestamp']
    if logs.exists() and order_column and int(order_column) < len(colums):
        col_name = colums[int(order_column)]
        if order_dir == 'desc':
            logs = logs.order_by('-%s' % col_name)
        else:
            logs = logs.order_by('%s' % col_name)
    
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1
    
    try:
        page = int(data.get('start', '0')) / length + 1
    except ValueError:
        page = 1
    
    count = len(logs)
    
    paginator = Paginator(logs, length)
    
    try:
        logs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        logs = paginator.page(paginator.num_pages)
    
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    for d in logs.object_list:
        t = TemplateResponse(request, 'blog/admin_log_ajax.html', {'d': d})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
    return HttpResponse(json.dumps(rs), content_type="application/json")

############################################################
@login_required
def tag(request):
    form = ShowForm()
    if request.method == "POST":
        return add_tag(request, Tag, TagForm, "admin_tag")
    return render(request, template_name="blog/tag.html", context={
        "model": "tag",
        "model_name": u"标签",
        "form": form,
    })

@login_required
def category(request):
    form = ShowForm()
    if request.method == "POST":
        return add_tag(request, Category, CategoryForm, "admin_category")
    return render(request, template_name="blog/tag.html", context={
        "model": "category",
        "model_name": u"分类",
        "form": form,
    })

def add_tag(request, model, form, reverse_name):
    status = request.POST.get('status', "")
    if status == "delete":
        id = request.POST.get('id', "")
        obj = model.objects.filter(pk=id).first()
        obj.delete()
        messages.add_message(request, messages.SUCCESS, u'删除成功')
    if status == "add":
        name = request.POST.get('name', "")
        f = form({'name': name})
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
        else:
            if f['name'].errors:
                msg = f['name'].errors.data[0].message % {}
            else:
                msg = _(u"未知错误，请重试。") % {}
            messages.add_message(request, messages.ERROR, msg)
    return HttpResponseRedirect(reverse(reverse_name))

@login_required
def ajax_tag(request):
    return ajax_lists(request, Tag)

@login_required
def ajax_category(request):
    return ajax_lists(request, Category)

def ajax_lists(request, model):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'name', 'created', 'updated']
    lists = model.objects.all()
    if search:
        lists = lists.filter(name__icontains=search)
    
    # if order_column and int(order_column) < len(colums):
    # if isinstance(query, query.QuerySet) and order_column and int(order_column) < len(colums):
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1
    
    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1
    
    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'blog/ajax_tag.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

############################################################
@login_required
def article(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = Article.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
            return HttpResponseRedirect(reverse("admin_article"))
    return render(request, template_name="blog/article.html", context={
    })

@login_required
def ajax_article(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'title', 'status', 'auth', 'source', 'views', 'likes', 'topped', 'created', 'updated', 'category']
    lists = Article.objects.all()
    if search:
        article_ids = list(ArticleTags.objects.filter(tag__name__icontains=search).values_list("article_id", flat=True))
        lists = lists.filter(
            Q(title__icontains=search) |
            Q(category__name__icontains=search) |
            Q( id__in=article_ids )
        )
    
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1
    
    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1
    
    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'blog/ajax_article.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

@login_required
def article_add(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse("admin_article"))
    return render(request, template_name="blog/article_add.html", context={
        "form": form,
        "is_instance": False,
    })

@login_required
def article_modify(request, article_id):
    obj = Article.objects.get(pk=article_id)
    form = ArticleForm(instance=obj, initial={"tags": obj.tags.all()})
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=obj)
        if form.is_valid():
            obj2 = form.save()
            form.referPicture(obj2)
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse("admin_article"))
    return render(request, template_name="blog/article_add.html", context={
        "form": form,
        "is_instance": True,
    })

@csrf_exempt
@login_required
def ckupload(request):
    callback = request.GET.get("CKEditorFuncNum")
    if request.method == 'POST' and request.FILES['upload']:
        fileobj = request.FILES['upload']
        content_type = fileobj.content_type
        size = fileobj.size
        fname = fileobj.name
        fext = os.path.splitext(fname)[-1]
        uuname = '{}-{}{}'.format(str(uuid.uuid1()), random.randint(1, 100000), fext)
        abspath_uri = "{}ckupload/{}".format(settings.MEDIA_URL, uuname)
        try:
            fname = fname.encode("utf-8")
        except BaseException as e:
            fname = uuname
            print e
        CKeditorPictureFile.objects.create(filename=fname, filetype=content_type, filepath=abspath_uri, filesize=size)
        with open(os.path.join(settings.MEDIA_ROOT, 'ckupload', uuname), 'w') as f:
            f.write(fileobj.read())
        res = r"<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'"+abspath_uri+"', '');</script>"
        return HttpResponse(res)
    raise Http404()


@login_required
def picture(request):
    if request.method == "POST":
        status = request.POST.get('status', "")
        if status == "delete":
            id = request.POST.get('id', "")
            obj = CKeditorPictureFile.objects.filter(article_id=0, pk=id).first()
            if obj: obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if status == "deleteall":
            ids = ( request.POST.get('ids', False) ).split(',')
            lists = CKeditorPictureFile.objects.filter(article_id=0, id__in=ids)
            for obj in lists:
                obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        return HttpResponseRedirect(reverse("admin_picture"))
    
    return render(request, template_name="blog/picture.html", context={
    })

@login_required
def ajax_picture(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'id', 'filename', 'filetype', 'filepath', 'filesize', 'article_id', 'id']
    lists = CKeditorPictureFile.objects.all()
    if search:
        lists = lists.filter(filename__icontains=search)
    
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1
    
    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1
    
    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'blog/ajax_picture.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

############################################################
@login_required
def comment(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = BlogComment.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
            return HttpResponseRedirect(reverse("admin_comment"))
    return render(request, template_name="blog/comment.html", context={
    })

@login_required
def ajax_comment(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'username', 'email', 'content', 'created', 'article']
    lists = BlogComment.objects.all()
    if search:
        lists = lists.filter(content__icontains=search)
    
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1
    
    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1
    
    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'blog/ajax_comment.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

############################################################
@login_required
def suggest(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = Suggest.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
            return HttpResponseRedirect(reverse("admin_suggest"))
    return render(request, template_name="blog/suggest.html", context={
    })

@login_required
def ajax_suggest(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'username', 'email', 'content', 'created']
    lists = Suggest.objects.all()
    if search:
        lists = lists.filter(suggest__icontains=search)
    
    if order_column and int(order_column) < len(colums):
        if order_dir == 'desc':
            lists = lists.order_by('-%s' % colums[int(order_column)])
        else:
            lists = lists.order_by('%s' % colums[int(order_column)])
    
    try:
        length = int(data.get('length', 1))
    except ValueError:
        length = 1
    
    try:
        start_num = int(data.get('start', '0'))
        page = start_num / length + 1
    except ValueError:
        start_num = 0
        page = 1
    
    count = lists.count()
    if start_num >= count:
        page = 1
    paginator = Paginator(lists, length)
    try:
        lists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lists = paginator.page(paginator.num_pages)
    rs = {"sEcho": 0, "iTotalRecords": count, "iTotalDisplayRecords": count, "aaData": []}
    re_str = '<td.*?>(.*?)</td>'
    number = length * (page-1) + 1
    for d in lists.object_list:
        t = TemplateResponse(request, 'blog/ajax_suggest.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")
