# -*- coding: utf-8 -*-
#

class DotDict(dict):
    '''用于操作 dict 对象

    >>> dd = DotDict(a=1, b=2)
    >>> dd.c = 3
    >>> dd
    {'a': 1, 'c': 3, 'b': 2}
    >>> del dd.c
    >>> dd
    {'a': 1, 'b': 2}
    '''

    Fields = tuple()

    def __getitem__(self, name):
        value = dict.__getitem__(self, name)
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        return value

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    __getattr__ = __getitem__
    # __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class BaseFormField(object):

    def __init__(self, value, error=None, is_strip=True):
        self.value = value
        if is_strip and isinstance(value, (basestring, str)):
            self.value = value.strip()
        self.error = error

    def set_error(self, error):
        self.error = error

class BaseCfilterActionFied(object):

    def __init__(self, id, action, field="", value="", sequence=999, error=None,
                 mail_sender="", mail_recipient="", mail_subject="", mail_type="html", mail_content_html="", mail_content_plain="", json_value=None):
        self.id = id
        self.action = action
        self.field = field
        self.value = value
        self.sequence=sequence
        self.error = error
        self.mail_sender = mail_sender
        self.mail_recipient = mail_recipient
        self.mail_subject = mail_subject
        self.mail_type = mail_type
        self.mail_content_html = mail_content_html
        self.mail_content_plain = mail_content_plain
        self.json_value = json_value

    def set_error(self, error):
        self.error = error


class BaseCfilterOptionFied(object):

    def __init__(self, id, parent_id="", logic="all", option="", suboption="", action="", value="", childs=None, error=None):
        self.id = id
        self.parent_id = parent_id
        self.logic = logic
        self.option = option
        self.suboption = suboption
        self.action = action
        self.value = value
        if childs is None:
            childs=[]
        self.childs = childs
        self.error = error

    def set_error(self, error):
        self.error = error


