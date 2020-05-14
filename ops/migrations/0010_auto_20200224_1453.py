# Generated by Django 2.1.12 on 2020-02-24 06:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0009_aliramlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='GtmDefaultLine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('default_line', models.GenericIPAddressField(default='1.1.1.1', verbose_name='普通路线解析地址，ip')),
                ('u_date', models.DateTimeField(auto_now=True, verbose_name='上次变动时间')),
            ],
        ),
        migrations.RemoveField(
            model_name='gtmcheckdomain',
            name='default_line',
        ),
        migrations.AddField(
            model_name='gtmdefaultline',
            name='Domain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ops.GtmCheckDomain'),
        ),
    ]