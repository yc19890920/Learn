from rest_framework import serializers
from ms.models import Tag, Category, Article

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id", "name"
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id", "name"
        ]

class ArticleSerializer(serializers.ModelSerializer):
    tag_id = serializers.IntegerField(required=False)
    category_id = serializers.IntegerField(required=False)
    tag_name = serializers.CharField(source='tag.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Article
        fields = [
            "id", "title", "content",
            "tag_id", "tag_name",
            "category_id", "category_name",
        ]


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=50, help_text=u'用户名')
    email = serializers.CharField(required=True, max_length=100, help_text=u'邮箱')

class EmptySerializer(serializers.Serializer):
    pass