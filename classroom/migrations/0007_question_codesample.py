# Generated by Django 2.0.4 on 2019-01-08 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_auto_20190108_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='codesample',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
