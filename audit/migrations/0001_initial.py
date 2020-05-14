# Generated by Django 2.1.12 on 2020-04-21 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryTaskAudit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('task', models.CharField(max_length=128, verbose_name='任务')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '队列任务日志',
                'verbose_name_plural': '队列任务日志',
            },
        ),
    ]
