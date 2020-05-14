# Generated by Django 2.1.12 on 2020-03-21 10:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0016_auto_20200320_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateShadowSocketTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('status', models.SmallIntegerField(default=1)),
                ('result', models.TextField(null=True, verbose_name='结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('vpn_template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ops.CreateShadowSocketTemplate')),
            ],
        ),
    ]
