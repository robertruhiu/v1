# Generated by Django 2.2 on 2019-08-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0023_auto_20190730_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='devrequest',
            name='eventcolor',
            field=models.CharField(default='blue', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='eventcolor',
            field=models.CharField(default='blue', max_length=100, null=True),
        ),
    ]
