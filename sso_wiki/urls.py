from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)


router.register(r'oss-wiki-login', views.OssWikiLoginView, basename='oss_wiki_login')
router.register(r'oss-wiki-sigup-check', views.OssWikiSigupCheckView, basename='oss_wiki_sigup_check')


app_name = 'sso_wiki'


urlpatterns = [
    path('', include(router.urls))
]
