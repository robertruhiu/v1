# Generated by Django 2.2 on 2020-06-19 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0051_auto_20200619_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
    ]
