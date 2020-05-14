# Generated by Django 2.1.12 on 2020-04-29 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aliecs', '0018_remove_aliuseraccesskey_project_permissions'),
        ('user', '0011_user_wiki_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=128, verbose_name='组名')),
                ('hosts_permission', models.BooleanField(default=True, verbose_name='此用户是否允许访问主机相关')),
                ('gtm_permission', models.BooleanField(default=True, verbose_name='此用户是否允许访问gtm切换')),
                ('cyt_iptables_permission', models.BooleanField(default=True, verbose_name='此用户是否允许访问cyt商户加白')),
                ('create_shadowsocket_permission', models.BooleanField(default=True, verbose_name='此用户是否允许创建shadowsocket')),
                ('create_forward_permission', models.BooleanField(default=True, verbose_name='此用户是否允许创建forward')),
                ('worktickets_permission', models.BooleanField(default=True, verbose_name='此用户是否允许访问工单')),
                ('wiki_permission', models.BooleanField(default=True, verbose_name='此用户是否允许访问wiki')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('project_permissions', models.ManyToManyField(blank=True, null=True, to='aliecs.AliUserAccessKey', verbose_name='阿里云主机访问权限')),
            ],
            options={
                'verbose_name': '权限组',
                'verbose_name_plural': '权限组',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='group_permissions',
            field=models.ManyToManyField(blank=True, null=True, to='user.PermissionGroup'),
        ),
    ]