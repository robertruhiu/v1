# Generated by Django 2.2 on 2019-08-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0025_auto_20190812_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentreport',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]