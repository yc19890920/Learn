from __future__ import unicode_literals
from django.utils import six
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import CharField, empty, ListField
from rest_framework.compat import (
    MaxLengthValidator, MaxValueValidator,
    MinLengthValidator, MinValueValidator, unicode_repr, unicode_to_repr
)

class IdsSplitField(CharField):
    default_error_messages = {
        'invalid': _('Not a valid string.'),
        'blank': _('This field may not be blank.'),
        'max_length': _('Ensure this field has no more than {max_length} characters.'),
        'min_length': _('Ensure this field has at least {min_length} characters.'),
        'split_flag': _('传入的ids不是正确的以英文逗号分割的字符串.')
    }
    initial = ''

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)
        self.split_flag = kwargs.pop('split_flag', True)
        super(IdsSplitField, self).__init__(**kwargs)
        if self.max_length is not None:
            message = lazy(
                self.error_messages['max_length'].format,
                six.text_type)(max_length=self.max_length)
            self.validators.append(
                MaxLengthValidator(self.max_length, message=message))
        if self.min_length is not None:
            message = lazy(
                self.error_messages['min_length'].format,
                six.text_type)(min_length=self.min_length)
            self.validators.append(
                MinLengthValidator(self.min_length, message=message))

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.
        if data == '' or (self.trim_whitespace and six.text_type(data).strip() == ''):
            if not self.allow_blank:
                self.fail('blank')
            return ''

        try:
            data = data or ""
            list(map(int, data.split(",")) if data else [])
        except:
            self.fail('split_flag')
        return super(CharField, self).run_validation(data)

    def to_internal_value(self, data):
        """
        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        if isinstance(data, str):
            data = data.split(",") if data else []
        try:
            data = data or ""
            return list(map(int, data) if data else [])
        except:
            self.fail('split_flag')