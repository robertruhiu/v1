# Generated by Django 2.2.21 on 2021-07-21 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20210630_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]