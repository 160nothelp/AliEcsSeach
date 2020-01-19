from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'check', views.CheckLoginView, basename='check')
router.register(r'index-base', views.IndexBaseView, basename='index_base')
router.register(r'change-password', views.ChangePasswordView, basename='change_password')


app_name = 'user'


urlpatterns = [
    path('login', obtain_jwt_token, name='login'),
    path('', include(router.urls)),
]
