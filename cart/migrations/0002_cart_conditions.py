# Generated by Django 2.2 on 2019-09-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='conditions',
            field=models.BooleanField(default=False),
        ),
    ]