from django.urls import path
from . import views


app_name = 'user'


urlpatterns = [
    path('login', views.LogInView.as_view(), name='login'),
    path('logout', views.LogOutView.as_view(), name='logout'),
    path('change-password', views.ChangePasswdView.as_view(), name='change_password'),
    path('check', views.CheckLogin.as_view(), name='check'),
]
