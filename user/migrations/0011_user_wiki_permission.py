# Generated by Django 2.1.12 on 2020-04-10 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_create_forward_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wiki_permission',
            field=models.BooleanField(default=True, verbose_name='此用户是否允许访问wiki'),
        ),
    ]
