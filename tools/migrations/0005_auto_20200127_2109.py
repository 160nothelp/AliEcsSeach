# Generated by Django 2.1.12 on 2020-01-27 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_auto_20200127_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(blank=True, upload_to='./tmp', verbose_name='上传文件'),
        ),
    ]
