# Generated by Django 2.0.4 on 2019-01-10 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_auto_20190110_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='transaction',
            field=models.IntegerField(),
        ),
    ]