# Generated by Django 2.2 on 2019-07-18 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0016_auto_20190508_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='tech_tags',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
