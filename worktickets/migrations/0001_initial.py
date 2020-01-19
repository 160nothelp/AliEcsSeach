# Generated by Django 2.1.12 on 2020-01-08 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='工单回复内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='工单回复时间')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='回复人')),
            ],
            options={
                'verbose_name': '工单回复',
                'verbose_name_plural': '工单回复',
            },
        ),
        migrations.CreateModel(
            name='TicketEnclosure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='附件上传时间')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='附件上传人')),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tools.Upload', verbose_name='附件')),
            ],
            options={
                'verbose_name': '工单附件',
                'verbose_name_plural': '工单附件',
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='工单类型')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '工单类型',
                'verbose_name_plural': '工单类型',
            },
        ),
        migrations.CreateModel(
            name='WorkTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=100, unique=True, verbose_name='工单编号')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='工单标题')),
                ('content', models.TextField(verbose_name='工单内容')),
                ('level', models.CharField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], default=2, max_length=3, verbose_name='工单等级')),
                ('ticket_status', models.CharField(choices=[(0, '未接收'), (1, '正在处理'), (2, '已解决'), (3, '搁置')], default=0, max_length=3, verbose_name='工单状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='工单创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='工单更新时间')),
                ('action_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='action_user', to=settings.AUTH_USER_MODEL, verbose_name='指派人')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('edit_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edit_user', to=settings.AUTH_USER_MODEL, verbose_name='处理人')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worktickets.TicketType', verbose_name='工单类型')),
            ],
            options={
                'verbose_name': '工单',
                'verbose_name_plural': '工单',
            },
        ),
        migrations.AddField(
            model_name='ticketenclosure',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worktickets.WorkTicket', verbose_name='工单'),
        ),
        migrations.AddField(
            model_name='ticketcomment',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worktickets.WorkTicket', verbose_name='工单'),
        ),
    ]