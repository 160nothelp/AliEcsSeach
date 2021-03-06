from django.utils.deprecation import MiddlewareMixin


class SetRemoteAddrFromForwardedFor(MiddlewareMixin):
    """
    如果部署了代理，使用此中间件获取远程客户端IP。
    在settings中注册该中间件。
    """
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError as err:
            print(err)
        else:
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip


# class DisableCSRFCheck(MiddlewareMixin):
#     def process_request(self, request):
#         setattr(request, '_dont_enforce_csrf_checks', True)

