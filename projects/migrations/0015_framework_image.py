# Generated by Django 2.2 on 2019-08-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20190820_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='framework',
            name='image',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
