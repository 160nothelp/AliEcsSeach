from rest_framework import serializers

from .models import MonitorHost, MonitorMemory, MonitorCpu, MonitorDisk


class MonitorCpuSerializer(serializers.ModelSerializer):
    host = serializers.SlugRelatedField(queryset=MonitorHost.objects.all(), slug_field='hostname')

    class Meta:
        model = MonitorCpu
        fields = ('time', 'usage_rate', 'host')


class MonitorMemorySerializer(serializers.ModelSerializer):
    host = serializers.SlugRelatedField(queryset=MonitorHost.objects.all(), slug_field='hostname')

    class Meta:
        model = MonitorMemory
        fields = ('time', 'usage', 'free', 'host')


class MonitorDiskSerializer(serializers.ModelSerializer):
    host = serializers.SlugRelatedField(queryset=MonitorHost.objects.all(), slug_field='hostname')

    class Meta:
        model = MonitorDisk
        fields = ('time', 'usage', 'free', 'host')

