# Generated by Django 2.1.12 on 2019-12-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0004_gtmcheckdomain_region_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='gtmcheckdomain',
            name='default_line',
            field=models.GenericIPAddressField(default='1.1.1.1', verbose_name='普通路线解析地址，ip'),
            preserve_default=False,
        ),
    ]
