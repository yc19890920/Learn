from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import F
from ms.models import Tag, Category, Article
from ms.serializers import TagSerializer, CategorySerializer, ArticleSerializer, UserSerializer, EmptySerializer
import random
import uuid
from django.db import connections, connection

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = ()

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()

class ArticleViewset(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = ()

    @action(detail=False, methods=['GET'], url_path='test', permission_classes=())
    def test(self, request):
        """  测试事物

        # 1. 不用事物的一个表的查询更新。
        read model._meta.app_label:ms, model._meta.model_name:tag
        write model._meta.app_label:ms, model._meta.model_name:tag
        read model._meta.app_label:ms, model._meta.model_name:category
        write model._meta.app_label:ms, model._meta.model_name:category

        # 2. 不用事物的两个表先查询后更新。
        read model._meta.app_label:ms, model._meta.model_name:category
        write model._meta.app_label:ms, model._meta.model_name:article
        write model._meta.app_label:ms, model._meta.model_name:article

        3. 使用事物的： 事物外面先查询，事物里面再更新。
        write model._meta.app_label:ms, model._meta.model_name:article
        write model._meta.app_label:ms, model._meta.model_name:article

        4. 使用事物的： 事物里面先查询，后更新。
        read model._meta.app_label:ms, model._meta.model_name:tag
        read model._meta.app_label:ms, model._meta.model_name:category
        write model._meta.app_label:ms, model._meta.model_name:article
        write model._meta.app_label:ms, model._meta.model_name:article



        using="default":
        # 1. 不用事物的一个表的查询更新。
        read model._meta.app_label:ms, model._meta.model_name:tag
        write model._meta.app_label:ms, model._meta.model_name:tag
        read model._meta.app_label:ms, model._meta.model_name:category
        write model._meta.app_label:ms, model._meta.model_name:category
        # 2. 不用事物的两个表先查询后更新。
        read model._meta.app_label:ms, model._meta.model_name:category
        write model._meta.app_label:ms, model._meta.model_name:article
        write model._meta.app_label:ms, model._meta.model_name:article
        3. 使用事物的： 事物外面先查询，事物里面再更新。
        write model._meta.app_label:ms, model._meta.model_name:article
        write model._meta.app_label:ms, model._meta.model_name:article
        4. 使用事物的： 事物里面先查询，后更新。
        read model._meta.app_label:ms, model._meta.model_name:tag
        read model._meta.app_label:ms, model._meta.model_name:category
        write model._meta.app_label:ms, model._meta.model_name:article
        write model._meta.app_label:ms, model._meta.model_name:article
        """

        try:
            Tag.objects.create(name="杨城11")
        except:
            pass

        print("# 1. 不用事物的一个表的查询更新。")
        tag = Tag.objects.filter(id=1).first()
        with transaction.atomic():
            if "杨城" in tag.name:
                tag.name = "杨城"
                tag.count = 10
                print("-----------1")
                tag.save()
            category = Category.objects.filter(name="杨城").first()
            category.name = "杨城"
            category.save()

        print("# 2. 不用事物的两个表先查询后更新。")
        category = Category.objects.filter(name="杨城").first()
        Article.objects.filter(tag=tag, category=category).update(title="1234")

        print("3. 使用事物的： 事物外面先查询，事物里面再更新。")
        with transaction.atomic(using="default"):
            Article.objects.filter(tag=tag, category=category).update(title="12345")

        print("4. 使用事物的： 事物里面先查询，后更新。")
        with transaction.atomic():
            tag = Tag.objects.filter(name="杨城").first()
            category = Category.objects.filter(name="杨城").first()
            Article.objects.filter(tag=tag, category=category).update(title="aaa")

        print("5. 边写边读。会报错。")
        with transaction.atomic():
            tag = Tag.objects.create(name=str(random.randint(1,10000)))
            # tag = Tag.objects.filter(pk=tag.id).first()
            tag.name = str(random.randint(1,10000))
            tag.save()
            print(tag.name)

        print("6. 跨数据库更新关系。会报错。查询加了 using('default')不会报错。")
        tags = Tag.objects.filter(name__icontains="杨城").using("default")
        # tags = Tag.objects.filter(name__icontains="杨城")
        with transaction.atomic():
            a = Article.objects.create(
                title="1", content="1"
            )
            a.count = F("count") + 1
            a.tag = tags[0]
            a.save()
            for tag in tags:
                tag.count = F("count") - 1
                tag.save()

        print("7. 跨数据库更新关系。不会会报错。")
        tags = Tag.objects.filter(name__icontains="杨城")
        art = Article.objects.filter(id=1).first()
        art.tag = tags[0]
        art.save()

        print("8. 跨数据库更新关系。不会会报错。")
        tags = Tag.objects.filter(name__icontains="杨城")
        Article.objects.filter(id=1).update(tag=tags[0])

        print("9. 跨数据库更新关系。会报错。查询加了 using('default')不会报错。")
        tags = Tag.objects.filter(name__icontains="杨城").using("default")
        # tags = Tag.objects.filter(name__icontains="杨城")
        a = Article.objects.create(
            title="1", content="1"
        )
        a.count = F("count") + 1
        a.tag = tags[0]
        a.save()
        for tag in tags:
            tag.count = F("count") - 1
            tag.save()

        print("10. 直接操作数据库，默认会使用default。")
        # cr = connections['default'].cursor()
        cr = connection.cursor()
        sql = """
        select * from ms_tag limit 1;
        update ms_tag set name='杨城a' where id=1;
        """
        cr.execute(sql)

        return Response("success", status=status.HTTP_200_OK)


from rest_framework.views import APIView
from ms.models import create_user_model
# User = create_user_model("test")

class UserViewset(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()
    lookup_field = 'username'
    lookup_value_regex = '.*'

    def create(self, request):
        """ 创建用户
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        username = data['username']
        email = data['email']
        User = create_user_model(username)
        if User.objects.filter(username=username).using("default").exists():
            return Response({"username": "用户名已存在"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create(username=username, email=email)
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, username=None):
        """ 获取用户
        """
        data = {}
        if username:
            User = create_user_model(username)
            u = User.objects.filter(username=username).first().using("default")
            data = {"username": u.username, "email": u.email} if u else {}
        if data:
            return Response(data)
        return Response({
            "detail": u'not found',
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='bcreate', serializer_class=EmptySerializer)
    def bcreate(self, request, *args, **kwargs):
        """ 批量创建
        """
        count = 1
        while count<=64:
            username = str(uuid.uuid4())
            User = create_user_model(username)
            if User.objects.filter(username=username).using("default").exists():
                continue
            count += 1
            User.objects.create(username=username, email=username)
        return Response(status=status.HTTP_200_OK)



