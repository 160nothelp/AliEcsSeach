from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import requests
from django.conf import settings
from django.utils.decorators import method_decorator

from user.user_permission import WikiPermissions


User_ = get_user_model()


class OssWikiLoginView(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def list(self, request, *args, **kwargs):
        username = request.user.username
        user = User_.objects.get(username=username)
        return Response({
            'username': username,
            'password': user.password
        })


class OssWikiSigupCheckView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    @method_decorator(WikiPermissions)
    def create(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        r = requests.get('%s%s/%s/' % (settings.WIKI_LOGIN_API, username, password))
        if r.status_code == 433:
            r = requests.get('%s%s/%s/' % (settings.WIKI_SIGUP_API, username, password))
            if r.status_code == 233:
                status_ = r.status_code
            elif r.status_code == 201:
                status_ = 201
            else:
                status_ = 490
        else:
            status_ = r.status_code
        return Response({
            'status': status_
        })
