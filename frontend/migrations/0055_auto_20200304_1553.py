# Generated by Django 2.2 on 2020-03-04 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0054_resources_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='resources',
            name='dislikes',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AlterField(
            model_name='resources',
            name='likes',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
    ]