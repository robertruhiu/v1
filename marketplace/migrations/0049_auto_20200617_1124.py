# Generated by Django 2.2 on 2020-06-17 11:24

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0048_auto_20200612_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developerreport',
            name='grading',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]