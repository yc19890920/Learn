# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from app.setting.models import MailCfilterRule
from app.setting.forms import SystemSetForm, MailCfilterRuleForm

@login_required
def systemSet(request):
    form = SystemSetForm()
    if request.method == "POST":
        form = SystemSetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u"修改配置成功")
            return HttpResponseRedirect(reverse('system_set'))
    return render(request, template_name="setting/set.html", context={
        "form": form,
    })

#########################################
# 邮件过滤
@login_required
def cfilter(request):
    if request.method == "POST":
        id = request.POST.get('id', "")
        status = request.POST.get('status', "")
        if status == "delete":
            obj = MailCfilterRule.objects.filter(pk=id).first()
            obj.delete()
            messages.add_message(request, messages.SUCCESS, u'删除成功')
        if status == "active":
            obj = MailCfilterRule.objects.filter(pk=id).first()
            obj.disabled=-1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'启用成功')
        if status == "disabled":
            obj = MailCfilterRule.objects.filter(pk=id).first()
            obj.disabled=1
            obj.save()
            messages.add_message(request, messages.SUCCESS, u'禁用成功')
        return HttpResponseRedirect(reverse('cfilter_set'))

    return render(request, "setting/cfilter.html", context={
    })

@login_required
def cfilter_add(request):
    form = MailCfilterRuleForm()
    if request.method == "POST":
        form = MailCfilterRuleForm(post=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'添加成功')
            return HttpResponseRedirect(reverse('cfilter_set'))
    return render(request, "setting/cfilter_add.html", context={
        "form": form,
    })

@login_required
def cfilter_modify(request, rule_id):
    obj = MailCfilterRule.objects.get(id=rule_id)
    form = MailCfilterRuleForm(instance=obj)
    if request.method == "POST":
        form = MailCfilterRuleForm(post=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, u'修改成功')
            return HttpResponseRedirect(reverse('cfilter_set'))
    return render(request, "setting/cfilter_add.html", context={
        "form": form,
    })

@login_required
def ajax_cfilter(request):
    data = request.GET
    order_column = data.get('order[0][column]', '')
    order_dir = data.get('order[0][dir]', '')
    search = data.get('search[value]', '')
    colums = ['id', 'name', 'type', 'logic', 'id', 'id', 'sequence', 'disabled']
    lists = MailCfilterRule.objects.all()
    if search:
        lists = lists.filter( name__icontains=search )

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
        t = TemplateResponse(request, 'setting/ajax_cfilter.html', {'d': d, 'number': number})
        t.render()
        rs["aaData"].append(re.findall(re_str, t.content, re.DOTALL))
        number += 1
    return HttpResponse(json.dumps(rs), content_type="application/json")

# 查看 条件或动作
@login_required
def cfilter_view(request, rule_id):
    status = request.GET.get('status', '')
    obj = MailCfilterRule.objects.get(id=rule_id)
    if status == "option":
        lists = obj.getOptions()
    elif status == "action":
        lists= obj.getActions()
    else:
        lists=[]
    return render(request, "setting/cfilter_view.html", context={
        "obj": obj,
        "status": status,
        "lists": lists,
    })