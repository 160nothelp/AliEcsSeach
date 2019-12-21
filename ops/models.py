from django.db import models
import uuid


class GtmCheckDomain(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    nick_name = models.CharField(max_length=12, verbose_name='名称标识')
    domain_list = models.TextField(verbose_name='一行一个域名，最多1000个')
    special_domain = models.TextField(verbose_name='特殊域名')
    gtm_cname = models.CharField(max_length=64, verbose_name='要解析的gtm_cname地址')
    default_line = models.GenericIPAddressField(verbose_name='普通路线解析地址，ip', default='1.1.1.1')
    AccessKey_ID = models.CharField(max_length=128, verbose_name='AccessKeyID')
    Access_Key_Secret = models.CharField(max_length=128, verbose_name='Access_KeySecret')
    region_id = models.CharField(max_length=64, verbose_name='地区ID')
    task_id = models.TextField(blank=True, null=True, verbose_name='阿里云任务id，不可手动填写')
    u_date = models.DateTimeField(auto_now=True, verbose_name='上次变动时间')

    def __str__(self):
        return '%s ------>  %s' % (self.nick_name, self.u_date)

    class Meta:
        verbose_name = 'gtm域名表'
        verbose_name_plural = 'gtm域名表'


# class GtmMonitor(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     name = models.CharField(max_length=64, verbose_name='名称标识')
#     AccessKey_ID = models.CharField(max_length=128, verbose_name='AccessKeyID')
#     Access_Key_Secret = models.CharField(max_length=128, verbose_name='Access_KeySecret')
#     region_id = models.CharField(max_length=64, verbose_name='地区ID')
#     ip_number = models.IntegerField(verbose_name='备用ip数量，需要与当前gtm线路池内的ip数量相同')
#     gtm_name = models.CharField(max_length=64, verbose_name='gtm名字')
#     gtm_id = models.CharField(max_length=64, verbose_name='gtm实例id')
#     image_id = models.CharField(max_length=64, verbose_name='镜像id')
#
#     def __str__(self):
#         return '%s ------>  %s' % (self.name, self.gtm_name)
#
#     class Meta:
#         verbose_name = 'gtm监控'
#         verbose_name_plural = 'gtm监控'
#
#
# class GtmIpPool(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     gtm = models.ForeignKey('GtmMonitor', related_name='ip_pool', on_delete=models.CASCADE)
#     ip = models.GenericIPAddressField(verbose_name='备用ip')
#     is_use = models.BooleanField(default=False, verbose_name='是否正在使用')
#     is_bad = models.BooleanField(default=False, verbose_name='是否被弃')
#
#     class Meta:
#         verbose_name = 'gtm_ip池'
#         verbose_name_plural = verbose_name
#
#
# class SercurityGroup(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     gtm = models.ForeignKey('GtmMonitor', related_name='sercurity', on_delete=models.CASCADE)
#     sercurity_id = models.CharField(max_length=64, verbose_name='安全组id')
#
#     class Meta:
#         verbose_name = 'gtm_安全组'
#         verbose_name_plural = verbose_name






