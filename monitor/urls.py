from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'monitor-cpu', views.MonitorCpuView, basename='monitor_cpu')
router.register(r'monitor-memory', views.MonintorMemoryView, basename='monitor_memory')
router.register(r'monitor-disk', views.MonitorDiskView, basename='monitor_disk')


app_name = 'monitor'


urlpatterns = [
    path('', include(router.urls)),
    path('monitor-socket', views.monitor_socket, name='cpu_monitor_socket')
]

