# Generated by Django 2.2 on 2020-02-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200210_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprisedeveloperreport',
            name='code_base',
            field=models.URLField(blank=True, null=True),
        ),
    ]