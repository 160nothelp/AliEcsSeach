from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'check', views.CheckLoginViewPermissionView, basename='check')
router.register(r'index-base', views.IndexBaseView, basename='index_base')
router.register(r'change-password', views.ChangePasswordView, basename='change_password')
router.register(r'users', views.UserViewSet, basename='users')


app_name = 'user'


urlpatterns = [
    path('login', obtain_jwt_token, name='login'),
    path('', include(router.urls)),
]
