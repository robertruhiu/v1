# Generated by Django 2.2 on 2020-06-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_enterprisedeveloper_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprisedeveloper',
            name='slug',
            field=models.SlugField(blank=True, default='', editable=False, null=True, unique=True),
        ),
    ]