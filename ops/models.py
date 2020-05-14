from django.db import models
import uuid

from aliecs.models import AliUserAccessKey
from user.models import User


class GtmCheckDomain(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    nick_name = models.CharField(max_length=12, verbose_name='名称标识')
    domain_list = models.TextField(verbose_name='一行一个域名，最多1000个')
    special_domain = models.TextField(verbose_name='特殊域名')
    gtm_cname = models.CharField(max_length=64, verbose_name='要解析的gtm_cname地址')
    # line = models.ForeignKey('GtmDefaultLine', on_delete=models.SET_NULL, null=True)
    # default_line = models.GenericIPAddressField(verbose_name='普通路线解析地址，ip', default='1.1.1.1')
    AccessKey_ID = models.CharField(max_length=128, verbose_name='AccessKeyID')
    Access_Key_Secret = models.CharField(max_length=128, verbose_name='Access_KeySecret')
    region_id = models.CharField(max_length=64, verbose_name='地区ID')
    task_id = models.TextField(blank=True, null=True, verbose_name='阿里云任务id，不可手动填写')
    u_date = models.DateTimeField(auto_now=True, verbose_name='上次变动时间')

    def __str__(self):
        return '%s ------>  %s' % (self.nick_name, self.u_date)

    class Meta:
        verbose_name = 'CM_GTM域名表'
        verbose_name_plural = verbose_name


class GtmDefaultLine(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    domain = models.ForeignKey('GtmCheckDomain', on_delete=models.SET_NULL, null=True)
    host_name = models.CharField(max_length=128, verbose_name='线路名称')
    default_line = models.GenericIPAddressField(verbose_name='普通路线解析地址，ip', default='1.1.1.1')
    u_date = models.DateTimeField(auto_now=True, verbose_name='上次变动时间')

    def __str__(self):
        return '%s ---------------- %s ------>  %s' % (self.host_name, self.default_line, self.u_date)
    
    class Meta:
        verbose_name = 'CM_GTM_默认线路表'
        verbose_name_plural = verbose_name


class AliRamLink(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    project_name = models.CharField(max_length=64, verbose_name='项目名称')
    ali_link = models.TextField(verbose_name='项目阿里云地址')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return '%s' % self.project_name

    class Meta:
        verbose_name = '项目阿里云子账号地址'
        verbose_name_plural = verbose_name


class TmpCytWhiteIpTables(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    white_ip = models.GenericIPAddressField(verbose_name='白名单ip')
    result = models.TextField(verbose_name='结果', null=True)
    status = models.SmallIntegerField(verbose_name='执行状态', default=1)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    
    def __str__(self):
        return '%s' % self.white_ip
    
    class Meta:
        verbose_name = 'cytIP白名单'
        verbose_name_plural = verbose_name


class TmpCytMerchNginx(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hosts_name = models.GenericIPAddressField(verbose_name='cyt商户nginx主机ip地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return '%s' % self.hosts_name
    
    class Meta:
        verbose_name = 'cyt商户白名单nginx'
        verbose_name_plural = verbose_name


class CreateShadowSocketTemplate(models.Model):
    InstanceChargeTypeChoise = {
        'PrePaid': '包年包月',
        'PostPaid': '按量付费',
    }

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    version = models.CharField(max_length=16, unique=True, verbose_name='模板版本号')
    project = models.ForeignKey(AliUserAccessKey, verbose_name='项目选择', on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='shadowsocketproject')
    security_id = models.CharField(max_length=128, verbose_name='vpn安全组id')
    admin_security_id = models.CharField(max_length=128, null=True,
                                         blank=True, verbose_name='需要加白vpnIP的admin安全组id')
    admmin_security_alikey = models.ForeignKey(AliUserAccessKey, verbose_name='需要加白vpnIP的admin安全组对应的阿里云key和地区',
                                               on_delete=models.SET_NULL, null=True, blank=True,
                                               related_name='admin_serurity')
    img_id = models.CharField(max_length=128, verbose_name='vpn镜像id')
    secret_key = models.CharField(max_length=128, verbose_name='秘钥对名称')
    vswitch_id = models.CharField(max_length=128, verbose_name='交换机id')
    vpn_port = models.CharField(max_length=12, verbose_name='vpn端口')
    vpn_password = models.CharField(max_length=128, verbose_name='vpn密码')
    InstanceChargeType = models.CharField(max_length=24, choices=tuple(InstanceChargeTypeChoise.items()),
                                          default='PostPaid', verbose_name='机器付费方式')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '%s >>>  %s' % (self.project, self.version)

    class Meta:
        verbose_name = 'shadowsocket vpn 创建模板'
        verbose_name_plural = verbose_name


class CreateShadowSocketTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    vpn_template = models.ForeignKey(CreateShadowSocketTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.SmallIntegerField(default=1)
    amount = models.SmallIntegerField(default=1)
    vpn_ip = models.TextField(blank=True, null=True)
    _false = models.TextField(null=True, blank=True)
    result = models.TextField(verbose_name='结果', null=True, default='0')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')


class CreateForwardTemplate(models.Model):
    InstanceChargeTypeChoise = {
        'PrePaid': '包年包月',
        'PostPaid': '按量付费',
    }

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    version = models.CharField(max_length=16, unique=True, verbose_name='模板版本号')
    project = models.ForeignKey(AliUserAccessKey, verbose_name='项目选择', on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='forwardproject')
    security_id = models.CharField(max_length=128, verbose_name='forward安全组id')
    img_id = models.CharField(max_length=128, verbose_name='forward镜像id')
    secret_key = models.CharField(max_length=128, verbose_name='秘钥对名称')
    vswitch_id = models.CharField(max_length=128, verbose_name='交换机id')
    forward_port = models.CharField(max_length=12, verbose_name='squid端口')
    InstanceChargeType = models.CharField(max_length=24, choices=tuple(InstanceChargeTypeChoise.items()),
                                          default='PostPaid', verbose_name='机器付费方式')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '%s >>>  %s' % (self.project, self.version)

    class Meta:
        verbose_name = 'forward 创建模板'
        verbose_name_plural = verbose_name


class CreateForwardTask(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    forward_template = models.ForeignKey(CreateForwardTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.SmallIntegerField(default=1)
    amount = models.SmallIntegerField(default=1)
    forward_pip = models.TextField(blank=True, null=True)
    forward_iip = models.TextField(blank=True, null=True)
    _false = models.TextField(null=True, blank=True)
    result = models.TextField(verbose_name='结果', null=True, default='0')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')


