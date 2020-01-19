from django.urls import path, include
from rest_framework import routers

from .views import UploadViewSet


router = routers.DefaultRouter(trailing_slash=False)


router.register(r'upload', UploadViewSet)


app_name = 'tools'


urlpatterns = [
    path('', include(router.urls)),
]
