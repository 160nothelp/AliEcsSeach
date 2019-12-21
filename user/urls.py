from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views


app_name = 'user'


urlpatterns = [
    path('login', views.LogInView.as_view(), name='login'),
    path('login_', obtain_jwt_token, name='login'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('change-password', views.ChangePasswdView.as_view(), name='change_password'),
    path('check', views.CheckLogin.as_view(), name='check'),
]
