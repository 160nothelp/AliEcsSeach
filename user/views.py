from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from user.api_session import gen_token
from user.api_session import authenticate as authenticate_
from .form import ChangepwdForm
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


class LogInView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    'status': 'y',
                    'token': gen_token(user.id)
                })
            else:
                message = '账号未启用，请联系管理员'
                return JsonResponse({
                    'status': 'a'
                })
        else:
            message = '登陆失败，账号或密码错误'
            return JsonResponse({
                'status': 'u'
            })


class LogOutView(View):
    @method_decorator(authenticate_)
    def get(self, request):
        auth_logout(request)
        return JsonResponse({
            'logout': True,
        })


class ChangePasswdView(View):
    @method_decorator(authenticate_)
    def post(self, request):
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpasswd')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpasswd1')
                user.set_password(newpassword)
                user.save()
                return JsonResponse({
                    'Status': 'ok'
                })
            return JsonResponse({
                'Status': 'erroroldpasswd'
            })
        return JsonResponse({
            'Status': 'newpasswdnosame'
        })


class CheckLogin(View):
    @method_decorator(authenticate_)
    def get(self, request):
        username = request.user.username
        obj = User.objects.get(username=username)
        return JsonResponse({
            'gtm_permission': obj.gtm_permission,
            'hosts_permission': obj.hosts_permission
        })


