# Generated by Django 2.2 on 2019-09-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190918_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='availabilty',
            field=models.CharField(max_length=30, null=True),
        ),
    ]