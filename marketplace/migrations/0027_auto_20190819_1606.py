# Generated by Django 2.2 on 2019-08-19 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0026_auto_20190816_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devrequest',
            name='candidatename',
        ),
        migrations.RemoveField(
            model_name='devrequest',
            name='company',
        ),
        migrations.RemoveField(
            model_name='devrequest',
            name='name',
        ),
        migrations.RemoveField(
            model_name='jobapplication',
            name='candidatename',
        ),
        migrations.RemoveField(
            model_name='jobapplication',
            name='company',
        ),
        migrations.RemoveField(
            model_name='jobapplication',
            name='name',
        ),
    ]
