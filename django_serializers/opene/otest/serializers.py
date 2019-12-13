from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from otest.models import Test
from django.utils.translation import ugettext_lazy as _

# 测试Serializer
class IdsSerializer(serializers.Serializer):
    ids = serializers.ListField(required=False, allow_empty=True, allow_null=True, help_text=u'ID列表')

    def validate(self, attrs):
        ids = attrs.get('ids', None)
        if not ids:
            attrs["ids"] = []
        return attrs

# 测试Serializer
class IdsActionSerializer(serializers.Serializer):
    ids = serializers.ListField(required=False, allow_empty=True, allow_null=True, help_text=u'ID列表')
    action = serializers.ChoiceField(choices=(
        ('disable', u'批量禁用id列表'),
        ('enable', u'批量禁用id列表'),
        ('delete', u'批量刪除id列表'),
    ),
        write_only=True, required=True,
        help_text=u'将要执行的操作')

    def validate(self, attrs):
        ids = attrs.get('ids', None)
        if not ids:
            attrs["ids"] = []
        return attrs

# 测试ModelSerializer
class TestSerializer(serializers.ModelSerializer):
    # user_id = serializers.HiddenField()
    name = serializers.CharField(
        required=True, max_length=50,
        error_messages={
            "blank": _("请输入名称"),
            "required": _("请输入名称"),
            "max_length": _("名称已超过50个字符。"),
            "min_length": _("名称少于1个字符。"),
        },
        validators=[
            UniqueValidator(
                queryset=Test.objects.all(),
                message=_("名称已存在！")
            )
        ]
    )
    # created = serializers.DateTimeField(write_only=True)
    # updated = serializers.DateTimeField(write_only=True)

    class Meta:
        model = Test
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Test.objects.all(),
                fields=('email', 'order_no'),
                message=_(u"邮箱和订单号唯一")
            ),
        ]
        # validators = []  # Remove a default "unique together" constraint.

    def validate_province(self, province):
        if not self.partial and not province:
            raise serializers.ValidationError(_("省/州不能为空！"))
        return province

    def validate_name2(self, name2):
        if not self.partial and not name2:
            raise serializers.ValidationError(_("name2不能为空！"))
        return name2

    def validate(self, attrs):
        province = attrs.get("province", None)
        name2 = attrs.get("name2", None)
        if not self.partial:
            if not name2:
                raise serializers.ValidationError({'name2': _("name2不能为空！")})
            if not province:
                raise serializers.ValidationError({'province': _("省/州不能为空！")})
        return attrs