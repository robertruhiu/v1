# Generated by Django 2.2 on 2019-08-09 15:05

from django.db import migrations
import separatedvaluesfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20190809_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_tags',
            field=separatedvaluesfield.models.SeparatedValuesField(blank=True, max_length=150, null=True),
        ),
    ]
