from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'celery-task-log', views.CeleryTaskAuditView, basename='celery_task_log')


app_name = 'audit'


urlpatterns = [
    path('', include(router.urls)),
]
