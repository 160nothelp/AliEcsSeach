# Generated by Django 2.1.12 on 2020-03-22 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0020_auto_20200322_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='createshadowsockettemplate',
            name='InstanceChargeType',
            field=models.CharField(choices=[('PrePaid', '包年包月'), ('PostPaid', '按量付费')], default='PostPaid', max_length=24, verbose_name='机器付费方式'),
        ),
    ]
