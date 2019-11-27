# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import json
from django import forms
from app.blog.models import Tag, Category, Article, Suggest, BlogComment, CKeditorPictureFile
from django.utils.translation import ugettext_lazy as _
from libs.tools import clearHtmlTags
from auditlog.models import AuditlogContentype, AUDITLOG_EXTEND_TYPE

P = re.compile('^(\w|[-+=.])+@\w+([-.]\w+)*\.(\w+)$')
PicP = re.compile(ur'src="(\/media\/ckupload\/.*?)"')

class AdminLogForm(forms.Form):
    start_time = forms.DateTimeField(label=_(u'开始时间'), required=False)
    end_time = forms.DateTimeField(label=_(u'结束时间'), required=False)
    content_type = forms.ChoiceField(label=_(u'类型'), required=False, initial="")

    def __init__(self, *args, **kwargs):
        super(AdminLogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'style': 'width: 170px;'})

        content_types = []
        lists = AuditlogContentype.objects.all()
        for o in lists:
            content_types.append((o.content_type_id, o.model_class))
        content_types.extend(list(AUDITLOG_EXTEND_TYPE))
        content_types.insert(0, ('', _(u'所有')))
        self.fields['content_type'].choices = content_types

class ShowForm(forms.Form):
    name_bak = forms.CharField(label=_(u'名称'), max_length=20, required=True)
    # name_bak = forms.CharField(_(u'名称'), required=True, max_length=20)

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError(_(u"输入为空，操作失败"))
        if Tag.objects.exclude(id=self.instance.pk).filter(name=name).exists():
            raise forms.ValidationError(_(u"重复添加，添加失败"))
        return name

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError(_(u"输入为空，操作失败"))
        if Category.objects.exclude(id=self.instance.pk).filter(name=name).exists():
            raise forms.ValidationError(_(u"重复添加，添加失败"))
        return name

class ArticleForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        label=_(u'标签'),
        queryset=None,
        # queryset=Tag.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={
            "data-placeholder": _(u"请选择或输入查询"),
            "autocomplete": "off",
            "class": "select2 ",
        }), help_text=_(u"可选多个标签"))

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset=Tag.objects.all()

    def clean_title(self):
        data = self.cleaned_data['title'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写标题"))
        return data

    def clean_content(self):
        data = self.cleaned_data['content'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写正文"))
        return data

    def clean_auth(self):
        data = self.cleaned_data['auth'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写作者"))
        return data

    def clean_abstract(self):
        data = self.cleaned_data['abstract'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写摘要"))
        return data

    def referPicture(self, obj):
        article_id = obj.id
        abstract = self.cleaned_data['abstract']
        content = self.cleaned_data['content']
        lists = PicP.findall(content)
        lists2 = PicP.findall(abstract)
        l = list( set(lists) | set(lists2) )
        CKeditorPictureFile.objects.filter(article_id=article_id).update(article_id=0)
        for i in l:
            objpic = CKeditorPictureFile.objects.filter(filepath=i).first()
            objpic.article_id = article_id
            objpic.save()

    class Meta:
        model = Article
        fields = ["title", "content",  "abstract", 'auth',  'source', "status", "topped", 'category', 'tags']


class SuggestForm(forms.ModelForm):

    def clean_username(self):
        data = self.cleaned_data['username'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写您的姓名"))
        return data

    def clean_content(self):
        data = self.cleaned_data['content'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写您的留言"))
        return data

    def clean_email(self):
        data = self.cleaned_data['email'].strip()
        if not  P.match(data):
            raise forms.ValidationError(_(u"请填写正确的邮箱"))
        return data

    class Meta:
        model = Suggest
        fields = ["username", "email", "content"]

        # widgets = {
        #     'content': forms.Textarea(attrs={
        #         'placeholder': u'写下你的意见吧~',
        #         'class': 'form-control',
        #         'rows': 4,
        #         'cols': 80,
        #     })
        # }

class BlogCommentForm(forms.ModelForm):

    article = forms.CharField(label=_(u'文章'), required=False, widget=forms.HiddenInput())

    def __init__(self, article, *args, **kwargs):
        super(BlogCommentForm, self).__init__(*args, **kwargs)
        self.article = article

    def clean_article(self):
        return self.article

    def clean_username(self):
        data = self.cleaned_data['username'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写您的姓名"))
        return data

    def clean_content(self):
        data = self.cleaned_data['content'].strip()
        if not data:
            raise forms.ValidationError(_(u"请填写您的留言"))
        return data

    def clean_email(self):
        data = self.cleaned_data['email'].strip()
        if not  P.match(data):
            raise forms.ValidationError(_(u"请填写正确的邮箱"))
        return data

    class Meta:
        model = BlogComment
        fields = ["article", "username", "email", "content"]
