# Generated by Django 2.2 on 2019-08-29 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0035_auto_20190828_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
