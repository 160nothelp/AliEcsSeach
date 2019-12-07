from django.db import models
import uuid


class GtmCheckDomain(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    nick_name = models.CharField(max_length=12, verbose_name='名称标识')
    domain_list = models.TextField(verbose_name='一行一个域名，最多1000个')
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
