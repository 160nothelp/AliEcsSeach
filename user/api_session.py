from django.http import JsonResponse
import jwt
import datetime
from django.conf import settings


def gen_token(user_id):
    # exp 设定过期的时间
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + 60*60*2
    }, settings.SECRET_KEY).decode()


def authenticate(fc):
    def wrapper(request):
        token = request.META.get('HTTP_X_CSRFTOKEN')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user_id = payload['user_id']
            request.user_id = user_id
        except Exception as e:
            return JsonResponse({
                'nologin': True
            })
        return fc(request)
    return wrapper

