from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from aliecs.models import AliUserAccessKey


class User(AbstractUser):
    hosts_permission = models.BooleanField(verbose_name='此用户是否允许访问主机相关', default=True)
    gtm_permission = models.BooleanField(verbose_name='此用户是否允许访问gtm切换', default=True)
    cyt_iptables_permission = models.BooleanField(verbose_name='此用户是否允许访问cyt商户加白', default=True)
    create_shadowsocket_permission = models.BooleanField(verbose_name='此用户是否允许创建shadowsocket', default=True)
    create_forward_permission = models.BooleanField(verbose_name='此用户是否允许创建forward', default=True)
    worktickets_permission = models.BooleanField(verbose_name='此用户是否允许访问工单', default=True)
    wiki_permission = models.BooleanField(verbose_name='此用户是否允许访问wiki', default=True)
    project_permissions = models.ManyToManyField(AliUserAccessKey, null=True, blank=True, verbose_name='阿里云主机访问权限')
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class PermissionGroup(models.Model):
    group_name = models.CharField(max_length=128, verbose_name='组名')
    user = models.ManyToManyField(User, null=True, blank=True, verbose_name='用户')
    hosts_permission = models.BooleanField(verbose_name='此用户是否允许访问主机相关', default=True)
    gtm_permission = models.BooleanField(verbose_name='此用户是否允许访问gtm切换', default=True)
    cyt_iptables_permission = models.BooleanField(verbose_name='此用户是否允许访问cyt商户加白', default=True)
    create_shadowsocket_permission = models.BooleanField(verbose_name='此用户是否允许创建shadowsocket', default=True)
    create_forward_permission = models.BooleanField(verbose_name='此用户是否允许创建forward', default=True)
    worktickets_permission = models.BooleanField(verbose_name='此用户是否允许访问工单', default=True)
    wiki_permission = models.BooleanField(verbose_name='此用户是否允许访问wiki', default=True)
    project_permissions = models.ManyToManyField(AliUserAccessKey, null=True, blank=True, verbose_name='阿里云主机访问权限')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')


    class Meta:
        verbose_name = "权限组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name

