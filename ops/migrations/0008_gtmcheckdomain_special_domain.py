# Generated by Django 2.1.12 on 2019-12-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0007_auto_20191205_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='gtmcheckdomain',
            name='special_domain',
            field=models.TextField(default='123.123', verbose_name='特殊域名'),
            preserve_default=False,
        ),
    ]
