# Generated by Django 2.1.12 on 2020-03-23 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_cyt_iptables_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='create_shadowsocket_permission',
            field=models.BooleanField(default=True, verbose_name='此用户是否允许创建shadowsocket'),
        ),
    ]
