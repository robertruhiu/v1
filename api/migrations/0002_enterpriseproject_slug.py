# Generated by Django 2.2 on 2020-01-14 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterpriseproject',
            name='slug',
            field=models.SlugField(default='', editable=False),
        ),
    ]