# Generated by Django 2.1.12 on 2020-04-29 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20200429_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='group_permissions',
        ),
        migrations.AddField(
            model_name='user',
            name='group_permissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.PermissionGroup'),
        ),
    ]