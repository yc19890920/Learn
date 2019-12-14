from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework.decorators import action

from otest.models import Test
from otest.serializers import TestSerializer, IdsSerializer, IdsActionSerializer, TestActionSerializer

class TestViewset(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = ()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TestSerializer
        elif self.action in ("disable_test", "enable_test"):
            return IdsSerializer
        elif self.action == "test_actions":
            return TestActionSerializer
        return TestSerializer

    def get_queryset(self):
        return Test.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        """ 列表 """
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ 删除 """
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """ 获取 """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """ 创建 """
        print(request.content_type)
        print("===================")
        print(request.data, type(request.data))
        data = request.data
        import pprint
        pprint.pprint(data)
        # user = self.request.user
        # data.update(mailbox=user, email=user.username, type='out')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """ 更新 """
        data = request.data
        # user = self.request.user
        # data.update(mailbox=user, email=user.username, type='out')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='actions', permission_classes=(), serializer_class=IdsActionSerializer)
    def test_actions(self, request):
        """ 批量禁用SMTP外发代理 """
        # user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        detail = serializer.save()
        return Response(detail, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='disable', permission_classes=(), serializer_class=IdsSerializer)
    def disable_test(self, request):
        """ 批量禁用SMTP外发代理 """
        # user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']
        if ids:
            Test.objects.filter(id__in=ids).update(disabled="1")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='enable', permission_classes=(), serializer_class=IdsSerializer)
    def enable_test(self, request):
        """ 批量启用SMTP外发代理 """
        # user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']
        if ids:
            Test.objects.filter(id__in=ids).update(disabled="-1")
        return Response(status=status.HTTP_204_NO_CONTENT)





