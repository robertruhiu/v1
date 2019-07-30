# Generated by Django 2.2 on 2019-07-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0021_auto_20190730_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devrequest',
            old_name='interview',
            new_name='interviewendtime',
        ),
        migrations.RenameField(
            model_name='jobapplication',
            old_name='interview',
            new_name='interviewendtime',
        ),
        migrations.AddField(
            model_name='devrequest',
            name='interviewstarttime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='interviewstarttime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
