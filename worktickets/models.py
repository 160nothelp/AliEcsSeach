from django.db import models
import uuid

from user.models import User
from tools.models import Upload


class TicketType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name=u'工单类型')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'工单类型'
        verbose_name_plural = u'工单类型'


class WorkTicket(models.Model):

    TicketLevel = {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
    }

    TicketStatus = {
        0: '未接收',
        1: '正在处理',
        2: '已解决',
        3: '搁置',
    }

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    pid = models.CharField(max_length=100, unique=True, verbose_name=u'工单编号')
    name = models.CharField(max_length=100, blank=True, verbose_name=u'工单标题')
    type = models.ForeignKey('TicketType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单类型')
    content = models.TextField(verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='create_user', verbose_name=u'创建者')
    action_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='action_user', verbose_name=u'指派人')
    edit_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edit_user', verbose_name=u'处理人')
    level = models.CharField(max_length=3, choices=tuple(TicketLevel.items()), default=2, verbose_name=u'工单等级')
    ticket_status = models.CharField(max_length=3, choices=tuple(TicketStatus.items()), default=0, verbose_name=u'工单状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'工单更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'工单'
        verbose_name_plural = u'工单'


class TicketComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ticket = models.ForeignKey(WorkTicket, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单')
    content = models.TextField(verbose_name=u'工单回复内容')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'回复人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'工单回复时间')

    class Meta:
        verbose_name = u'工单回复'
        verbose_name_plural = u'工单回复'


class TicketEnclosure(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ticket = models.ForeignKey(WorkTicket, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'工单')
    file = models.ForeignKey(Upload, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件')
    create_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u'附件上传人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'附件上传时间')

    class Meta:
        verbose_name = u'工单附件'
        verbose_name_plural = u'工单附件'




