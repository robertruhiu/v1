# Generated by Django 2.2 on 2019-08-26 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0031_auto_20190826_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='projectstarttime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]