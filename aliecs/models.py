from django.db import models
import uuid


class AliUserAccessKey(models.Model):
    nickname = models.CharField(max_length=64, unique=True, verbose_name='账号标识名称')
    AccessKey_ID = models.CharField(max_length=128, verbose_name='AccessKeyID')
    Access_Key_Secret = models.CharField(max_length=128, verbose_name='Access_KeySecret')
    region_id = models.CharField(max_length=64, verbose_name='地区ID')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '阿里云认证信息'
        verbose_name_plural = '阿里云认证信息'


class OtherPlatforms(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    nickname = models.CharField(max_length=64, unique=True, verbose_name='标识名称')
    the_other = models.BooleanField(default=True)
    hosts = models.ManyToManyField('OtherPlatformsHosts', verbose_name="主机")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '其他机器信息'
        verbose_name_plural = '其他机器信息'


class OtherPlatformsHosts(models.Model):

    os_type = (
        ('linux', 'linux'),
        ('windows', 'windows'),
    )

    status_type = (
        ('运行', '运行'),
        ('停止', '停止'),
        ('下线', '下线'),
    )

    InstanceId = models.UUIDField(default=uuid.uuid4, primary_key=True)
    InstanceName = models.CharField(max_length=64, verbose_name='主机名称')
    OSType = models.CharField(choices=os_type, max_length=12, default='linux', verbose_name='os类型')
    PublicIpAddress = models.GenericIPAddressField(verbose_name='公网IP', default='0.0.0.0')
    PrivateIpAddress = models.GenericIPAddressField(verbose_name='内网IP', default='127.0.0.1')
    ZoneId = models.CharField(max_length=128, verbose_name='地区', default='地球')
    Status = models.CharField(choices=status_type, max_length=64, default='运行', verbose_name='状态')
    InstanceNetworkType = models.CharField(max_length=64, verbose_name='网络类型', default='集线器')
    Cpu = models.SmallIntegerField(verbose_name='cpu核数', default=1)
    Memory = models.SmallIntegerField(verbose_name='内存大小', default=1)
    InstanceChargeType = models.CharField(max_length=64, verbose_name='购买或续费方式', default='包月')
    InternetMaxBandwidthOut = models.CharField(max_length=64, verbose_name='出口带宽(Mbps)', default='4')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<%s：%s--%s>' % (self.InstanceName, self.PublicIpAddress, self.PrivateIpAddress)

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '其他机器列表'
        verbose_name_plural = '其他机器列表'


class HostIpSearchTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user_type = models.CharField(max_length=64)
    allip = models.GenericIPAddressField()
    result = models.TextField()
    status = models.SmallIntegerField()
    p_time = models.DateTimeField(auto_now=True)
    c_time = models.DateTimeField(auto_now_add=True)

