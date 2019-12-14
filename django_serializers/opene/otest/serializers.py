from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from opene.rest_framework.validators import UniqueTogetherValidator
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

# 自定义 Serializer 保存逻辑
class TestActionSerializer(IdsActionSerializer):

    def save(self):
        validated_data = self.validated_data
        ids = validated_data['ids']
        action = validated_data['action']
        message = None
        if ids:
            if action == 'delete':
                Test.objects.filter(id__in=ids).delete()
                message = _("批量删除成功")
            elif action == 'disable':
                Test.objects.filter(id__in=ids).update(disabled="1")
                message = _("批量禁用成功")
            elif action == 'enable':
                Test.objects.filter(id__in=ids).update(disabled="-1")
                message = _("批量启用成功成功")
        return message

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
        ],
        label=_("名称"), help_text=_("名称")
    )

    order_no = serializers.CharField(
        required=True, max_length=50,
        error_messages={
            "blank": _("请输入订单号"),
            "required": _("请输入订单号"),
            "max_length": _("订单号已超过50个字符。"),
            "min_length": _("订单号少于1个字符。"),
        },
        label=_("订单号"), help_text=_("订单号")
    )

    # created = serializers.DateTimeField(write_only=True)
    # updated = serializers.DateTimeField(write_only=True)

    class Meta:
        model = Test
        fields = '__all__'
        # fields = ("name", "gender", "birthday", "email", "mobile")
        # fields = '__all__': 表示所有字段
        # exclude = ('add_time',):  除去指定的某些字段
        # 这三种方式，存在一个即可
        validators = [
            UniqueTogetherValidator(
                queryset=Test.objects.all(),
                fields=('email', 'order_no'),
                message={"order_no": _(u"邮箱和订单号唯一")}
            ),
        ]
        # validators = []  # Remove a default "unique together" constraint.
        # error_messages = {
        #     "name": {
        #         "blank": _("请输入名称"),
        #         "required": _("请输入名称"),
        #         "max_length": _("名称已超过50个字符。"),
        #         "min_length": _("名称少于1个字符。"),
        #     },
        #     "order_no": {
        #         "blank": _("请输入订单号"),
        #         "required": _("请输入订单号"),
        #         "max_length": _("订单号已超过50个字符。"),
        #         "min_length": _("订单号少于1个字符。"),
        #     }
        # }

    def validate_province(self, province):
        if not self.partial and not province:
            raise serializers.ValidationError(_("省/州不能为空！"))
        return province

    def validate_name2(self, name2):
        if not self.partial and not name2:
            raise serializers.ValidationError(_("name2不能为空！"))
        return name2

    def validate(self, attrs):
        print("===================partial", self.partial)
        print(attrs)
        # province = attrs.get("province", None)
        # name2 = attrs.get("name2", None)
        # if not self.partial:
        #     if not name2:
        #         raise serializers.ValidationError({'name2': _("name2不能为空！")})
        #     if not province:
        #         raise serializers.ValidationError({'province': _("省/州不能为空！")})

        # del attrs["code"]
        return attrs

    def create(self, validated_data):
        """
        传入验证过的数据, 创建并返回`Tag`实例。
        """
        name = validated_data['name']
        if Test.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": '名称 %(name)s 已存在！' % {'name': name}})
        return super().create(validated_data)
        # instance = Test.objects.create(**validated_data)
        # return instance

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        # if validated_data['name']:
        #     instance.name = validated_data['name']
        # instance.save()
        # return instance