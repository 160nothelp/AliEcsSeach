# Generated by Django 2.1.12 on 2019-12-04 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0003_gtmcheckdomain_nick_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gtmcheckdomain',
            name='region_id',
            field=models.CharField(default=1234, max_length=64, verbose_name='地区ID'),
            preserve_default=False,
        ),
    ]
