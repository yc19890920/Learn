from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
 
from serializers import UserSerializer
from app.core.models import User
 
 
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('password', 'nick')