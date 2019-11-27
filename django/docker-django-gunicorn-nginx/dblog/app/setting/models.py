# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import models
from django.template import Template, Context
from app.setting import choices
from app.core.models import Department
from libs.formats import dict_compatibility, safe_format

class MailCfilterRule(models.Model):
    """ 新的内容过滤器规则表 """
    name = models.CharField(u"规则名称", max_length=150, null=True, blank=True, help_text=u"管理员输入的规则备注，可不填")
    type = models.IntegerField(u"类型", choices=choices.FILTER_RULE, default=-1, null=False, blank=False)
    logic = models.CharField(u"条件关系", max_length=50, default="all", choices=choices.RULE_LOGIC, null=False, blank=False,
                             help_text=u"all：满足所有条件，one：满足一条即可")
    sequence = models.IntegerField(u"规则优先级", default=999, null=False, blank=False)
    disabled = models.IntegerField(u'状态', choices=choices.DISABLED_STATUS, default=-1, null=False, blank=False)

    class Meta:
        db_table = "mail_cfilter"

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.deleteOptions()
        self.deleteActions()
        super(MailCfilterRule, self).delete(using, keep_parents)

    def deleteOptions(self):
        MailCfilterRuleOption.objects.filter(rule_id=self.id).delete()

    def deleteActions(self):
        MailCfilterRuleAction.objects.filter(rule_id=self.id).delete()

    def getActions(self):
        return MailCfilterRuleAction.objects.filter(rule_id=self.id).order_by("sequence")

    def getOptions(self, parent_id=0):
        return MailCfilterRuleOption.objects.filter(rule_id=self.id, parent_id=parent_id)

class MailCfilterRuleOption(models.Model):
    """ 条件组表 """
    rule_id = models.IntegerField(u"所属规则", default=0, db_index=True, null=False, blank=False,
                                  help_text=u"所属节点，ext_cfilter_rule_new的主键")
    parent_id = models.IntegerField(u"父ID", db_index=True, default=0, null=False, blank=False, help_text=u"这个条件的父亲ID，逻辑关系由parent_id指向的那一行决定")
    logic = models.CharField(u"逻辑表达式", max_length=50, choices=choices.COND_LOGIC, default="all", null=False, blank=False, help_text=u"all:并且,one：或")
    option = models.CharField(u"条件1", max_length=50, null=False, blank=False, choices=choices.ALL_CONDITION_OPTION)
    suboption = models.CharField(u"条件2", max_length=50, null=False, blank=False)
    # suboption = models.CharField(u"条件2", max_length=50, null=False, blank=False, choices=constants.ALL_CONDITION_SUBOPTION)
    action = models.CharField(u"动作", max_length=50, null=False, blank=False, choices=choices.ALL_CONDITION_ACTION)
    value = models.CharField(u"值", max_length=500, null=True, blank=True)

    class Meta:
        db_table = "mail_cfilter_option"

    def view_html(self):
        load_html = self.template_string
        t = Template(load_html)
        htmls = [ t.render(Context( {"obj": self, "parent": True} )) ]
        for d in self.Children:
            htmls.append(
                t.render(Context( {"obj": d, "parent": False} ))
            )
        return "".join(htmls)

    @property
    def template_string(self):
        return u"""
        <div class="col-sm-12">
            {% if parent %}
                <input class="col-xs-2 col-sm-2" value="{{ obj.get_logic_display }}" disabled/>
            {% else %}
                <label class="col-xs-2 col-sm-2"></label>
            {% endif %}
            <input class="col-xs-2 col-sm-2" value="{{ obj.suboption_display }}" disabled/>
            <input class="col-xs-2 col-sm-2" value="{{ obj.get_action_display }}" disabled/>
            <input class="col-xs-4 col-sm-4" value="{{ obj.value_display }}" disabled/>
        </div>
        """

    @property
    def Children(self):
        return MailCfilterRuleOption.objects.filter(parent_id=self.id)

    @property
    def suboption_display(self):
        if self.option in ("header", "extra"):
            d = dict(choices.ALL_CONDITION_SUBOPTION)
            if self.suboption in d:
                return d[self.suboption]
        return self.suboption

    @property
    def value_display(self):
        d = dict(choices.ALL_CONDITION_SUBOPTION)
        if self.option in ("header", "extra"):
            if self.suboption in choices.G_COND_OPTION_IN:
                try:
                    value = int(self.value)
                except:
                    value = 0
                obj = Department.objects.filter(id=value).first()
                return obj and obj.title or ""
            elif self.suboption in choices.G_COND_OPTION_GTE:
                try:
                    value = int(self.value)
                except:
                    value = 0
                return u"{}M".format(value)
            elif self.suboption in choices.G_COND_OPTION_EQ:
                if self.value == "1":
                    return u'是'
                else:
                    return u'否'
            elif self.suboption in choices.G_COND_OPTION_OTHER:
                return self.value
            else:
                return self.value
        return ""

class MailCfilterRuleAction(models.Model):
    """ 新的内容过滤器动作表 """
    rule_id = models.IntegerField(u"所属规则", default=0, db_index=True, null=False, blank=False,
                                  help_text=u"所属节点，ext_cfilter_rule_new的主键")
    action = models.CharField(u"动作", max_length=50, null=False, blank=False, choices=choices.ALL_ACTION)
    value = models.CharField(u"值", max_length=500, null=True, blank=True)
    sequence = models.IntegerField(u"动作优先级", default=999, null=False, blank=False)

    class Meta:
        db_table = "mail_cfilter_action"

    def view_html(self):
        T = '<div class="col-sm-12"><div class="hr hr-6 hr-dotted"></div></div>'
        load_html = self.template_string
        htmls = [ safe_format(load_html, **{ "name": u"动作", "value": self.get_action_display() }) ]
        htmls.append(T)
        htmls.append( safe_format(load_html, **{ "name": u"优先级", "value": self.sequence }) )

        j = self.json_value
        # if self.action in ("break", "flag", "label", "delete", "sequester"):
        #     pass
        if self.action in ("move_to", "copy_to"):
            d = dict(choices.CFILTER_ACTION_SELECT_VALUE)
            value = ""
            key = dict_compatibility(j, "value")
            if key in d:  value = d[key]
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"设置值", "value":  value }) )

        if self.action in ("jump_to", "forward", "delete_header", "append_body"):
            value = dict_compatibility(j, "value")
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"设置值", "value":  value }) )

        if self.action in ("append_header", ):
            field = dict_compatibility(j, "field")
            value = dict_compatibility(j, "value")
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"邮件头", "value":  field }) )
            htmls.append( safe_format(load_html, **{ "name": u"邮件头设置值", "value":  value }) )

        if self.action in ("mail", ):
            mail_sender = dict_compatibility(j, "sender")
            mail_recipient = dict_compatibility(j, "recipient")
            mail_subject = dict_compatibility(j, "subject")
            mail_type = dict_compatibility(j, "content_type")
            content = dict_compatibility(j, "content")
            if mail_type == "html":
                mail_type = "html内容"
            else:
                mail_type = "纯文本"
            htmls.append(T)
            htmls.append( safe_format(load_html, **{ "name": u"发信人", "value":  mail_sender }) )
            htmls.append( safe_format(load_html, **{ "name": u"收信人", "value":  mail_recipient }) )
            htmls.append( safe_format(load_html, **{ "name": u"主题", "value":  mail_subject }) )
            htmls.append( safe_format(load_html, **{ "name": u"类型", "value":  mail_type }) )
            htmls.append( safe_format(load_html, **{ "name": u"内容", "value":  content }) )
        return "".join(htmls)

    @property
    def template_string(self):
        return u"""<div class="col-sm-12"><label class="col-xs-2 col-sm-2">{name}：</label><label class="col-xs-10 col-sm-10 ">{value}</label></div>"""

    @property
    def json_value(self):
        try:
            return json.loads(self.value)
        except:
            return {}
