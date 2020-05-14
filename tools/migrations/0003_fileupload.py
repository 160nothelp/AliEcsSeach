# Generated by Django 2.1.12 on 2020-01-21 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_auto_20200108_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='./tmp', verbose_name='上传文件')),
            ],
            options={
                'verbose_name': '文件上传',
                'verbose_name_plural': '文件上传',
            },
        ),
    ]
