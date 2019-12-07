# Generated by Django 2.1.12 on 2019-12-04 12:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GtmCheckDomain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('domain_list', models.TextField(verbose_name='一行一个域名，最多1000个')),
                ('task_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='阿里云任务id，不可手动填写')),
                ('u_date', models.DateTimeField(auto_now=True, verbose_name='上次变动时间')),
            ],
            options={
                'verbose_name': 'gtm域名表',
                'verbose_name_plural': 'gtm域名表',
            },
        ),
    ]
