# Generated by Django 2.2 on 2020-10-27 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_codeln', '0011_auto_20201027_0729'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='withdraw',
            field=models.BooleanField(default=False),
        ),
    ]
