from django.http import JsonResponse

from .models import User


def HostsPermission(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        if not obj.hosts_permission:
            return JsonResponse({
                    'permission': 'denied'
                })
        return fc(request)
    return wrapper


def GtmPermission(fc):
    def wrapper(request):
        username = request.user.username
        obj = User.objects.get(username=username)
        if not obj.gtm_permission:
            return JsonResponse({
                    'permission': 'denied'
                })
        return fc(request)
    return wrapper

