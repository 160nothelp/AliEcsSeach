from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserPermissionSerializer, UserChangePasswordSerializer
from .models import User


User_ = get_user_model()


# 自定义用户登录认证，配合drf_jwt
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User_.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexBaseView(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def list(self, request, *args, **kwargs):
        username = request.user.username
        return Response({
            'username': username
        })


class ChangePasswordView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserChangePasswordSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=request.user.username, password=serializer.data.get("old_password"))
            if user is not None:
                user.set_password(serializer.data.get("new_password"))
                user.save()
                return Response("Success", status=status.HTTP_200_OK)
            else:
                return Response({'message': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckLoginView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserPermissionSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'gtm_permission': serializer.data[0]['gtm_permission'],
            'hosts_permission': serializer.data[0]['hosts_permission']
        })


