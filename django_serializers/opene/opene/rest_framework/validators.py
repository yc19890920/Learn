from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.validators import qs_exists, qs_filter, UniqueTogetherValidator


class UniqueTogetherValidator(UniqueTogetherValidator):
    """
    Validator that corresponds to `unique_together = (...)` on a model class.

    Should be applied to the serializer class, not to an individual field.
    """
    message = _('字段 {field_names} 必须进行唯一设置。')
    missing_message = _('必填字段.')

    def __init__(self, queryset, fields, message=None):
        if not isinstance(message, dict):
            raise Exception('错误消息使用格式错误')
        super().__init__(queryset, fields, message=message)

    def enforce_required_fields(self, attrs):
        """
        The `UniqueTogetherValidator` always forces an implied 'required'
        state on the fields it applies to.
        """
        if self.instance is not None:
            return
        # missing_items = {
        #     field_name: self.missing_message
        #     for field_name in self.fields
        #     if field_name not in attrs
        # }
        # if missing_items:
        #     raise ValidationError(missing_items, code='required')

    def __call__(self, attrs):
        self.enforce_required_fields(attrs)
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset)
        queryset = self.exclude_current_instance(attrs, queryset)

        # Ignore validation if any field is None
        checked_values = [
            value for field, value in attrs.items() if field in self.fields
        ]
        if None not in checked_values and qs_exists(queryset):
            # field_names = ', '.join(self.fields)
            # message = self.message.format(field_names=field_names)
            # raise ValidationError(message, code='unique')
            raise ValidationError(self.message, code='unique')