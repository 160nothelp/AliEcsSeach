# Generated by Django 2.1.12 on 2019-12-20 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aliecs', '0014_hostipsearchtask_allname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostipsearchtask',
            name='instancename',
        ),
    ]
