# Generated by Django 2.1.5 on 2019-04-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]