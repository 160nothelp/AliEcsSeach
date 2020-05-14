from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import requests
from django.conf import settings

from .serializers import UserPermissionSerializer, UserChangePasswordSerializer, UserSerializer
from .models import PermissionGroup
from .group_permission import ManyGroupPermissionCheck


User = get_user_model()


# 自定义用户登录认证，配合drf_jwt
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
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
                r = requests.get('%s%s/%s/%s/' % (settings.WIKI_CHANG_PASSWORD_API, request.user.username,
                                                  serializer.data.get("old_password"), serializer.data.get("new_password")))
                if r.status_code == 233:
                    return Response({'message': '修改成功，wiki密码修改失败'}, status=status.HTTP_200_OK)
                return Response("Success", status=status.HTTP_200_OK)
            else:
                return Response({'message': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckLoginViewPermissionView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserPermissionSerializer
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        try:
            group_permission_obj = ManyGroupPermissionCheck(
                PermissionGroup.objects.filter(user__username=self.request.user.username)
            )
            group_permission = group_permission_obj.permission_check()
            if serializer.data[0]['gtm_permission'] or group_permission['gtm_permission']:
                gtm_permission = True
            else:
                gtm_permission = False
            if serializer.data[0]['hosts_permission'] or group_permission['hosts_permission']:
                hosts_permission = True
            else:
                hosts_permission = False
            if serializer.data[0]['cyt_iptables_permission'] or group_permission['cyt_iptables_permission']:
                cyt_iptables_permission = True
            else:
                cyt_iptables_permission = False
            if serializer.data[0]['create_shadowsocket_permission'] or group_permission['create_shadowsocket_permission']:
                create_shadowsocket_permission = True
            else:
                create_shadowsocket_permission = False
            if serializer.data[0]['create_forward_permission'] or group_permission['create_forward_permission']:
                create_forward_permission = True
            else:
                create_forward_permission = False
            if serializer.data[0]['worktickets_permission'] or group_permission['worktickets_permission']:
                worktickets_permission = True
            else:
                worktickets_permission = False
            if serializer.data[0]['wiki_permission'] or group_permission['wiki_permission']:
                wiki_permission = True
            else:
                wiki_permission = False


            return Response({
                'gtm_permission': gtm_permission,
                'hosts_permission': hosts_permission,
                'cyt_iptables_permission': cyt_iptables_permission,
                'create_shadowsocket_permission': create_shadowsocket_permission,
                'create_forward_permission': create_forward_permission,
                'worktickets_permission': worktickets_permission,
                'wiki_permission': wiki_permission,
            })
        except Exception as e:
            return Response({'message': 'no_login'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    search_fields = ['username']
