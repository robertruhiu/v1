# Generated by Django 2.2 on 2020-03-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20200326_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterfeedback',
            name='slug',
            field=models.SlugField(blank=True, default='', null=True),
        ),
    ]
