# Generated by Django 2.2 on 2019-10-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0043_auto_20191007_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcenter',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testcenter',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
