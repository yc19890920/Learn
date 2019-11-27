# -*- coding: utf-8 -*-
import json
from app.core.models import Prefs
from libs.forms import DotDict, BaseFormField, BaseCfilterOptionFied, BaseCfilterActionFied

from django.utils.translation import ugettext, ugettext_lazy as _

from app.core.models import Department
from app.setting import choices as constants
from app.setting.models import MailCfilterRule, MailCfilterRuleOption, MailCfilterRuleAction
from libs.formats import dict_compatibility

class SystemSetForm(DotDict):

    Fields = (
        # field, defaulte, 描述
        (u'system_lang', '1',    u"系统语言设置, 1：中文，2：英文"),
        (u'mail_server', '',     u"邮件服务器设置"),
        (u'mail_port',   '25',   u"邮件服务器端口设置"),
        (u'mail_ssl',     '0',   u"邮件服务SSL设置，0：不是SSL发送，1：SSL发送"),
        (u'mail_sender', '',     u"邮件服务器发件人设置"),
        (u'mail_passwd', '',     u"邮件服务器发件人密码设置"),
        (u'mail_recipient', '', u"系统收件邮箱设置"),
    )

    def __init__(self, post=None):
        self.post = post
        self.is_post = False
        self.__initialize()
        self.__valid = True

    def __initialize(self):
        data = {}
        if self.post:
            data = self.post
            self.is_post = True
        for key, value, remark in self.Fields:
            if not self.is_post:
                value_ref = Prefs.geValue(name=key)
                value = value_ref if value_ref else value
            self[key] = BaseFormField(value=data.get(key, value), error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        for key, value, remark in self.Fields:
            obj = getattr(self, key)
            if key == "system_lang" and obj.value not in ('1', '2'):
                self.__valid = False
                obj.set_error(_(u"未知错误."))
            if key == "mail_ssl" and obj.value not in ('0', '1'):
                self.__valid = False
                obj.set_error(_(u"未知错误."))
            elif not obj.value:
                self.__valid = False
                obj.set_error(_(u"输入不能为空."))

    def save(self):
        for key, value, remark in self.Fields:
            obj = getattr(self, key)
            Prefs.saveValue(key, value=obj.value, remark=remark)


class MailCfilterRuleForm(object):

    ###########################################################
    # 动作列表
    ACTION_TYPE = constants.ALL_ACTION
    # 动作只有 action
    Action_only = ("break", "flag", "label", "delete", "sequester")


    # 动作有 action value
    # 动作有 action value 并下拉选择的
    Action_only_select = ("move_to", "copy_to")
    Action_only_slect_value = (
        ("Spam", u"垃圾箱"),
        ("Trash", u"废件箱"),
        ("Inbox", u"收件箱"),
        ("Sent", u"发件箱"),
    )
    # 动作有 action value  整型输入框
    Action_only_int = ("jump_to", )
    # 动作有 action value  字符串输入框
    Action_only_str = ("forward", "delete_header") # delete_header     value = { 'field':邮件头字段 }
    # 动作有 action value  编辑器
    Action_only_edit = ("append_body", )  #append_header     value = { 'field':邮件头字段, 'value':前端存入的值 }

    # 动作有 action field value
    Action_has_all = ("append_header", )

    # 动作复杂 mail
    Action_only_mail = ("mail", ) # value = { 'sender':发信人,'recipient':收信人,'subject':主题,'content':内容,'content_type':plain or html }
    Action_only_mail_type = (
        ("html", u"html内容"),
        ("plain", u"纯文本"),
    )

    ###########################################################
    # 条件列表
    COND_LOGIC = constants.COND_LOGIC
    # 条件类型
    ALL_CONDITION_SUBOPTION = constants.ALL_CONDITION_SUBOPTION
    #### 条件动作
    # 1. 可以为 not_in , in 的  option  # 部门下拉选择  3个
    G_COND_OPTION_IN_T = constants.G_COND_OPTION_IN_T
    G_COND_ACTION_IN_T = constants.G_COND_ACTION_IN_T
    G_COND_OPTION_IN = constants.G_COND_OPTION_IN
    G_COND_ACTION_IN = constants.G_COND_ACTION_IN

    # 可以为 >= , <= 的 option  邮件大小  1个
    G_COND_OPTION_GTE_T = constants.G_COND_OPTION_GTE_T
    G_COND_ACTION_GTE_T = constants.G_COND_ACTION_GTE_T
    G_COND_OPTION_GTE = constants.G_COND_OPTION_GTE
    G_COND_ACTION_GTE = constants.G_COND_ACTION_GTE

    # 特殊设置的 option 只能为 ==  2个
    G_COND_OPTION_EQ_T = constants.G_COND_OPTION_EQ_T
    G_COND_ACTION_EQ_T = constants.G_COND_ACTION_EQ_T
    G_COND_OPTION_EQ = constants.G_COND_OPTION_EQ
    G_COND_ACTION_EQ = constants.G_COND_ACTION_EQ
    G_COND_ACTION_EQ_VALUE = constants.G_COND_ACTION_EQ_VALUE

    # 通用
    G_COND_OPTION_OTHER_T = constants.G_COND_OPTION_OTHER_T
    G_COND_ACTION_OTHER_T = constants.G_COND_ACTION_OTHER_T
    G_COND_OPTION_OTHER = constants.G_COND_OPTION_OTHER
    G_COND_ACTION_OTHER = constants.G_COND_ACTION_OTHER

    # 自定义
    G_COND_OPTION_ALL = constants.G_COND_OPTION_ALL

    def __init__(self, instance=None, post=None):
        self.__instance = instance
        self.__post = post
        self.__valid = True
        self.__initialize()

    def is_valid(self):
        self.__check()
        return self.__valid

    def save(self):
        # 主表
        if self.__instance:
            obj = self.__instance
            obj.name = self.name.value
            obj.type = self.type.value
            obj.logic = self.logic.value
            obj.sequence = self.sequence.value
            obj.disabled = self.disabled.value
            obj.save()
        else:
            obj = MailCfilterRule.objects.create(
                name=self.name.value, type=self.type.value,
                logic=self.logic.value, sequence=self.sequence.value, disabled=self.disabled.value
            )

        rule_id = obj.id
        # 先删除
        obj.deleteOptions()
        obj.deleteActions()

        # 动作
        bulk_action = []
        for d in self.cfilteraction.value:
            bulk_action.append( MailCfilterRuleAction( rule_id=rule_id, action=d.action, value=d.json_value, sequence=d.sequence ))
        MailCfilterRuleAction.objects.bulk_create(bulk_action)

        # 条件
        for d in self.cfilteroption.value:
            option_obj = MailCfilterRuleOption.objects.create(
                rule_id=rule_id, logic=d.logic, option=d.option,
                suboption=d.suboption, action=d.action, value=d.value
            )
            for dd in d.childs:
                MailCfilterRuleOption.objects.create(
                    rule_id=rule_id, parent_id=option_obj.id, logic=d.logic, option=dd.option,
                    suboption=dd.suboption, action=dd.action, value=dd.value
                )

    def DepartMent(self):
        return Department.objects.all()

    def __check(self):
        pass

    def __initialize(self):
        if self.__post:
            post = self.__post
            name = post.get("name", "")
            error = None
            if not name:
                self.__valid = False
                error = u"规则名称不能为空"
            self.name = BaseFormField(value=name, error=error)
            self.sequence = BaseFormField(value=post.get("sequence", "999"), error=None)
            ltype = post.get("type", "-1").strip()
            ltype = int(ltype) if ltype in ("1", "-1") else 1
            self.type = BaseFormField(value=ltype, error=None)
            disabled = post.get("disabled", "-1").strip()
            disabled = int(disabled) if disabled in ("1", "-1") else -1
            self.disabled = BaseFormField(value=disabled, error=None)

            ###########################################################
            # 条件处理
            logic = self.__post.get("logic", "all").strip()
            logic = logic if logic in ("all", "one") else "all"
            self.logic = BaseFormField(value=logic, error=None)

            options = []
            opt_error = False
            cfilteroptions = post.getlist('cfilteroptions[]', '')
            cfilteroptionchilds = post.getlist('cfilteroptionchilds[]', '')
            for this_id in cfilteroptions:
                this_id_bak = this_id.replace("--", "")
                action = ""
                value = ""
                childs = []
                error = None
                logic = post.get("option_logic_type{}".format(this_id), "all").strip()
                suboption = post.get("option_suboption{}".format(this_id), "").strip()
                if suboption in constants.ALL_CONDITION_OPTION_HEADER_VALUE:
                    option = "header"
                else:
                    option = "extra"

                if suboption in self.G_COND_OPTION_IN:
                    action = post.get("option_action_dpt{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_IN:
                        error = _(u"未知错误！")
                        opt_error=True
                    try:
                        value = post.get("option_value_dpt{}".format(this_id), "").strip()
                    except:
                        value = 0

                if suboption in self.G_COND_OPTION_GTE:
                    action = post.get("option_action_size{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_GTE:
                        error = _(u"未知错误！")
                        opt_error=True
                    try:
                        value = int(post.get("option_value_size{}".format(this_id), "").strip())
                    except:
                        value = 0
                    if value <= 0:
                        error = _(u"邮件大小必须大于0！")
                        opt_error=True

                if suboption in self.G_COND_OPTION_EQ:
                    action = post.get("option_action_disabled{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_EQ:
                        error = _(u"未知错误！")
                        opt_error=True

                    value = post.get("option_value_disabled{}".format(this_id), "-1").strip()
                    if value not in ("-1", "1"):
                        error = _(u"未知错误！")
                        opt_error=True

                if suboption in self.G_COND_OPTION_OTHER:
                    action = post.get("option_action_other{}".format(this_id), "").strip()
                    if action not in self.G_COND_ACTION_OTHER:
                        error = _(u"未知错误！")
                        opt_error=True
                    value = post.get("option_value_other{}".format(this_id), "").strip()
                    if not value:
                        error = _(u"不能为空！")
                        opt_error=True

                if not suboption:
                    error = _(u"未知错误！")
                    opt_error=True

                format_c = "--{}".format(this_id_bak)
                this_childs = [ i for i in cfilteroptionchilds if i.endswith(format_c)]
                for this_child_id in this_childs:
                    sub_id = this_child_id.replace(format_c, "")
                    sub_action = ""
                    sub_value = ""
                    sub_error = None

                    sub_suboption = post.get("option_suboption{}".format(this_child_id), "").strip()
                    if sub_suboption in constants.ALL_CONDITION_OPTION_HEADER_VALUE:
                        sub_option = "header"
                    else:
                        sub_option = "extra"

                    if sub_suboption in self.G_COND_OPTION_IN:
                        sub_action = post.get("option_action_dpt{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_IN:
                            sub_error = _(u"未知错误！")
                            opt_error=True
                        try:
                            value = post.get("option_value_dpt{}".format(this_child_id), "").strip()
                        except:
                            value = 0

                    if sub_suboption in self.G_COND_OPTION_GTE:
                        sub_action = post.get("option_action_size{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_GTE:
                            sub_error = _(u"未知错误！")
                            opt_error=True
                        try:
                            sub_value = int(post.get("option_value_size{}".format(this_child_id), "").strip())
                        except:
                            sub_value = 0

                        if sub_value <= 0:
                            sub_error = _(u"邮件大小必须大于0！")
                            opt_error=True

                    if sub_suboption in self.G_COND_OPTION_EQ:
                        sub_action = post.get("option_action_disabled{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_EQ:
                            sub_error = _(u"未知错误！")
                            opt_error=True

                        sub_value = post.get("option_value_disabled{}".format(this_child_id), "-1").strip()
                        if sub_value not in ("-1", "1"):
                            sub_error = _(u"未知错误！")
                            opt_error=True

                    if sub_suboption in self.G_COND_OPTION_OTHER:
                        sub_action = post.get("option_value_other{}".format(this_child_id), "").strip()
                        if sub_action not in self.G_COND_ACTION_OTHER:
                            sub_error = _(u"未知错误！")
                            opt_error=True
                        sub_value = post.get("option_value_other{}".format(this_child_id), "").strip()
                        if not sub_value:
                            sub_error = _(u"输入不能为空！")
                            opt_error=True

                    if not sub_suboption:
                        sub_error = _(u"未知错误！")
                        opt_error=True

                    T1 = BaseCfilterOptionFied(
                        id=sub_id, parent_id=this_id_bak, logic=logic, option=sub_option, suboption=sub_suboption,
                        action=sub_action, value=sub_value, error=sub_error
                    )
                    childs.append(T1)

                T = BaseCfilterOptionFied(
                    id=this_id_bak, parent_id="", logic=logic, option=option, suboption=suboption,
                    action=action, value=value, error=error, childs=childs
                )
                options.append(T)

            if opt_error:
                self.__valid = False
            self.cfilteroption = BaseFormField(value=options, error=opt_error)

            ###########################################################
            # 动作处理
            acts=[]
            index = 1
            opt_error = False
            cfilteractionids = post.getlist('cfilteractionids[]', '')
            for rid in cfilteractionids:
                error = None
                field = ""
                value = ""
                mail_sender=""
                mail_recipient=""
                mail_subject=""
                mail_type="html"
                mail_content_html=""
                mail_content_plain=""
                sequence = post.get('action_sequence{}'.format(rid), "")
                json_value = json.dumps({"value": None})
                action_type = post.get('action_type{}'.format(rid), "")

                if action_type in self.Action_only_int:
                    value = post.get("action_value_int{}".format(rid), "0")
                    json_value = json.dumps({"value": value})

                if action_type in self.Action_only_select:
                    value = post.get("action_value_select{}".format(rid), "")
                    json_value = json.dumps({"value": value})

                # Action_only_str
                if action_type in self.Action_only_str:
                    value = post.get("action_value_b{}".format(rid), "").strip()
                    if not value:
                        error = _(u"不能为空！")
                        opt_error=True
                    json_value = json.dumps({"value": value})
                    if action_type == "delete_header":
                        json_value = json.dumps({"field": value})

                # 动作有 action value  编辑器
                if action_type in self.Action_only_edit:
                    value = post.get("action_value_edit{}".format(rid), "").strip()
                    if not value:
                        error = _(u"请在编辑器输入追加内容！")
                        opt_error=True
                    json_value = json.dumps({"value": value})

                if action_type in self.Action_has_all:
                    field = post.get("action_field{}".format(rid), "").strip()
                    value = post.get("action_value_a{}".format(rid), "").strip()
                    if not field:
                        error = _(u"邮件头设置不能为空！")
                        opt_error=True
                    if field and not value:
                        error = _(u"邮件头设置值不能为空！")
                        opt_error=True
                    json_value = json.dumps({"field": field, "value": value})

                # 动作复杂 mail
                if action_type in self.Action_only_mail:
                    mail_sender = post.get("action_value_mail_sender{}".format(rid), "").strip()
                    mail_recipient = post.get("action_value_mail_recipient{}".format(rid), "").strip()
                    mail_subject = post.get("action_value_mail_subject{}".format(rid), "").strip()
                    mail_type = post.get("action_value_mail_type{}".format(rid), "").strip()
                    mail_content_html = post.get("action_value_mail_content_html{}".format(rid), "").strip()
                    mail_content_plain = post.get("action_value_mail_content_plain{}".format(rid), "").strip()
                    content = ""
                    if not mail_sender:
                        error = _(u"发信人不能为空！")
                        opt_error=True
                    if not mail_recipient:
                        error = _(u"收信人不能为空！")
                        opt_error=True
                    if not mail_subject:
                        error = _(u"主题不能为空！")
                        opt_error=True
                    if mail_type == "html":
                        content = mail_content_html
                    elif mail_type == "plain":
                        content = mail_content_plain
                    if not content:
                        error = _(u"邮件内容不能为空！")
                        opt_error=True
                    json_value = json.dumps({'sender':mail_sender, 'recipient':mail_recipient,'subject':mail_subject,'content':content,'content_type': mail_type})

                acts.append( BaseCfilterActionFied(
                    id=index, action=action_type, field=field, value=value, error=error, sequence=sequence,
                    mail_sender=mail_sender, mail_recipient=mail_recipient, mail_subject=mail_subject, mail_type=mail_type,
                    mail_content_html=mail_content_html, mail_content_plain=mail_content_plain, json_value=json_value
                ) )
                index += 1

            if opt_error:
                self.__valid = False
            self.cfilteraction = BaseFormField(value=acts, error=opt_error)

        elif self.__instance:
            obj = self.__instance
            self.name =  BaseFormField(value=obj.name, error=None)
            self.sequence =  BaseFormField(value=obj.sequence, error=None)
            self.type =  BaseFormField(value=obj.type, error=None)
            self.disabled = BaseFormField(value=obj.disabled, error=None)
            self.logic = BaseFormField(value=obj.logic, error=None)

            actions = []
            for d in obj.getActions():
                field = ""
                value = ""
                mail_sender=""
                mail_recipient=""
                mail_subject=""
                mail_type="html"
                mail_content_html=""
                mail_content_plain=""

                action = d.action
                try:
                    j = json.loads(d.value)
                except:
                    j = {}
                if action == "delete_header":
                    field = dict_compatibility(j, "field")
                elif action == "append_header":
                    field = dict_compatibility(j, "field")
                    value = dict_compatibility(j, "value")
                elif action == "mail":
                    mail_sender = dict_compatibility(j, "sender")
                    mail_recipient = dict_compatibility(j, "recipient")
                    mail_subject = dict_compatibility(j, "subject")
                    mail_type = dict_compatibility(j, "content_type")
                    if mail_type == "html":
                        mail_content_html = dict_compatibility(j, "content")
                    else:
                        mail_content_plain = dict_compatibility(j, "content")
                else:
                    value = dict_compatibility(j, "value")
                    if action in self.Action_only_int:
                        try:
                            value = int(value)
                        except:
                            value = 0

                T = BaseCfilterActionFied(
                    id=d.id, action=d.action, field=field, value=value, error=None, sequence=d.sequence,
                    mail_sender=mail_sender, mail_recipient=mail_recipient, mail_subject=mail_subject, mail_type=mail_type,
                    mail_content_html=mail_content_html, mail_content_plain=mail_content_plain, json_value=j
                )
                actions.append(T)
            self.cfilteraction = BaseFormField(value=actions, error=None)

            options=[]
            for d in obj.getOptions():
                childs = []
                this_id = d.id
                logic = d.logic
                option = d.option
                suboption = d.suboption
                action = d.action
                value = d.value

                for dd in obj.getOptions(parent_id=this_id):
                    sub_id = dd.id
                    sub_parent_id = this_id
                    sub_logic = logic
                    sub_option = dd.option
                    sub_suboption = dd.suboption
                    sub_action = dd.action
                    sub_value = dd.value
                    T1 = BaseCfilterOptionFied(
                        id=sub_id, parent_id=sub_parent_id, logic=sub_logic, option=sub_option, suboption=sub_suboption,
                        action=sub_action, value=sub_value, error=None
                    )
                    childs.append(T1)

                T = BaseCfilterOptionFied(
                    id=this_id, parent_id="", logic=logic, option=option, suboption=suboption,
                    action=action, value=value, error=None, childs=childs
                )
                options.append(T)
            self.cfilteroption = BaseFormField(value=options, error=None)
        else:
            self.name = BaseFormField(value="", error=None)
            self.sequence = BaseFormField(value="999", error=None)
            self.type = BaseFormField(value=1, error=None)
            self.disabled = BaseFormField(value=-1, error=None)
            self.logic = BaseFormField(value="all", error=None)
            self.cfilteraction = BaseFormField(value=[ BaseCfilterActionFied(id=0, action="break"),], error=None)
            self.cfilteroption = BaseFormField(
                value=[
                    BaseCfilterOptionFied(
                        id=0, logic="all", option="extra", suboption="all_mail",
                        childs=[ BaseCfilterOptionFied(id=1, parent_id=0, logic="all", option="extra", suboption="all_mail", error=None) ] ) ],
                error=None)

