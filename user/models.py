from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    hosts_permission = models.BooleanField(verbose_name='此用户是否允许访问主机相关', default=True)
    gtm_permission = models.BooleanField(verbose_name='此用户是否允许访问gtm切换', default=True)

    class Meta(AbstractUser.Meta):
        pass