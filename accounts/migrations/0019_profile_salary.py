# Generated by Django 2.2 on 2019-09-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20190820_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='salary',
            field=models.IntegerField(null=True),
        ),
    ]
