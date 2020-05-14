from django.db import models
import uuid

from user.models import User


class CeleryTaskAudit(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='用户')
    task = models.CharField(max_length=128, verbose_name='任务')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'提交时间')

    def __str__(self):
        return '%s -------------->  %s' % (self.user, self.task)

    class Meta:
        verbose_name = '队列任务日志'
        verbose_name_plural = verbose_name
