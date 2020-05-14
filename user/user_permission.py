from django.http import JsonResponse, HttpResponse

from .models import User, PermissionGroup
from .group_permission import ManyGroupPermissionCheck


def HostsPermission(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        group_permission_obj = ManyGroupPermissionCheck(
            PermissionGroup.objects.filter(user=obj)
        )
        group_permission = group_permission_obj.permission_check()
        if obj.hosts_permission or group_permission['hosts_permission']:
            hosts_permission = True
        else:
            hosts_permission = False
        if not hosts_permission:
            # return JsonResponse({
            #         'permission': 'denied'
            #     })
            return HttpResponse(status=403)
        return fc(request)
    return wrapper


def GtmPermission(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        group_permission_obj = ManyGroupPermissionCheck(
            PermissionGroup.objects.filter(user=obj)
        )
        group_permission = group_permission_obj.permission_check()
        if obj.gtm_permission or group_permission['gtm_permission']:
            gtm_permission = True
        else:
            gtm_permission = False
        if not gtm_permission:
            # return JsonResponse({
            #         'permission': 'denied'
            #     })
            return HttpResponse(status=403)
        return fc(request)
    return wrapper


def CytIptablesPermission(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        group_permission_obj = ManyGroupPermissionCheck(
            PermissionGroup.objects.filter(user=obj)
        )
        group_permission = group_permission_obj.permission_check()
        if obj.cyt_iptables_permission or group_permission['cyt_iptables_permission']:
            cyt_iptables_permission = True
        else:
            cyt_iptables_permission = False
        if not cyt_iptables_permission:
            # return JsonResponse({
            #         'permission': 'denied'
            #     })
            return HttpResponse(status=403)
        return fc(request)
    return wrapper


def ProjectPermissions(fc):
    def wrapper(request):
        # try:
        #     username = request.user.username
        #     user = request.query_params.get('user')
        #     username_obj = User.objects.get(username=username)
        #     user_obj = username_obj.project_permissions.get(nickname=user)
        # except Exception as e:
        #     # return JsonResponse({
        #     #     'permission': 'denied'
        #     # })
        #     return JsonResponse({
        #         'index_data_': ''
        #     })
        username = request.user.username
        ali_user = request.query_params.get('user')
        username_obj = User.objects.get(username=username)
        ali_user_obj = username_obj.project_permissions.filter(nickname=ali_user)
        group_obj = PermissionGroup.objects.filter(user__username=username)
        status_f = False
        for group in group_obj:
            f = group.project_permissions.filter(nickname=ali_user)
            if f:
                status_f = True
        # group_ali_user_obj = group_obj.project_permissions.filter(nickname=ali_user)
        if not ali_user_obj and not status_f:
            return JsonResponse({
                'index_data_': ''
            })
        return fc(request)
    return wrapper


def ShadowsocketPermissions(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        group_permission_obj = ManyGroupPermissionCheck(
            PermissionGroup.objects.filter(user=obj)
        )
        group_permission = group_permission_obj.permission_check()
        if obj.create_shadowsocket_permission or group_permission['create_shadowsocket_permission']:
            create_shadowsocket_permission = True
        else:
            create_shadowsocket_permission = False
        if not create_shadowsocket_permission:
            # return JsonResponse({
            #     'permission': 'denied'
            # })
            return HttpResponse(status=403)
        return fc(request)
    return wrapper


def ForwardPermissions(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        if not obj.create_forward_permission:
            # return JsonResponse({
            #     'permission': 'denied'
            # })
            return HttpResponse(status=403)
        return fc(request)
    return wrapper


def WikiPermissions(fc):
    def wrapper(request):
        username = request.data['username']
        obj = User.objects.get(username=username)
        group_permission_obj = ManyGroupPermissionCheck(
            PermissionGroup.objects.filter(user=obj)
        )
        group_permission = group_permission_obj.permission_check()
        if obj.wiki_permission or group_permission['wiki_permission']:
            wiki_permission = True
        else:
            wiki_permission = False
        if not wiki_permission:
            return JsonResponse({
                'permission': 'pass'
            })
        return fc(request)
    return wrapper
