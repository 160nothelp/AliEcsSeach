# Generated by Django 2.1.12 on 2019-12-13 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aliecs', '0010_auto_20191212_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceNameResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameField(
            model_name='hostipsearchtask',
            old_name='instanceame',
            new_name='instancename',
        ),
        migrations.AddField(
            model_name='instancenameresult',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='aliecs.HostIpSearchTask'),
        ),
    ]