# Generated by Django 2.2 on 2021-03-05 13:08

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0058_jobapplication_relevance'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
    ]