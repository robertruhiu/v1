# Generated by Django 2.2 on 2019-07-22 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0009_auto_20190722_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devrequest',
            name='developers',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AlterField(
            model_name='devrequest',
            name='paid',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
    ]
