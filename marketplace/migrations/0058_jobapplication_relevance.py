# Generated by Django 2.2 on 2020-12-10 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0057_auto_20201204_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='relevance',
            field=models.IntegerField(default=0),
        ),
    ]
