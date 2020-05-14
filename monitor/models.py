from django.db import models
import uuid


class MonitorHost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ip = models.GenericIPAddressField(default='127.0.0.1', verbose_name='被监控端IP')
    hostname = models.CharField(max_length=128, verbose_name='主机名')
    u_date = models.DateTimeField(auto_now=True, verbose_name='上次变动时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return '%s -------------->  %s' % (self.hostname, self.ip)

    class Meta:
        verbose_name = '监控机器表'
        verbose_name_plural = verbose_name


class MonitorCpu(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    host =  models.ForeignKey(MonitorHost, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    usage_rate = models.CharField(max_length=8)


class MonitorMemory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    host = models.ForeignKey(MonitorHost, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    usage = models.CharField(max_length=8)
    free = models.CharField(max_length=8)


class MonitorDisk(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    host = models.ForeignKey(MonitorHost, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    usage = models.CharField(max_length=8)
    free = models.CharField(max_length=8)

