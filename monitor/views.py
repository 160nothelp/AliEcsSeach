from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from dwebsocket.decorators import accept_websocket, require_websocket
from django.utils.decorators import method_decorator
from rest_framework.response import Response
import json
from django.core import serializers

from .models import MonitorDisk, MonitorMemory, MonitorCpu
from .serializers import MonitorMemorySerializer, MonitorCpuSerializer, MonitorDiskSerializer


class MonitorCpuView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MonitorCpuSerializer
    queryset = MonitorCpu.objects.all().order_by('time')[:6]
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class MonintorMemoryView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MonitorMemorySerializer
    queryset = MonitorMemory.objects.all().order_by('time')[:1]
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


class MonitorDiskView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MonitorDiskSerializer
    queryset = MonitorDisk.objects.all().order_by('time')[:1]
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)


@accept_websocket
def monitor_socket(request):
    for message in request.websocket:
        cpu_monitor = MonitorCpu.objects.all().order_by('-time')[:6]
        memory_monitor = MonitorMemory.objects.all().order_by('-time')[:1]
        disk_monitor = MonitorDisk.objects.all().order_by('-time')[:1]
        cpu_monitor_data = serializers.serialize("json", cpu_monitor)
        memory_monitor_data = serializers.serialize("json", memory_monitor)
        disk_monitor_data = serializers.serialize("json", disk_monitor)
        request.websocket.send(json.dumps({'cpu_monitor_data': cpu_monitor_data,
                                           'memory_monitor_data': memory_monitor_data,
                                           'disk_monitor_data': disk_monitor_data}))

