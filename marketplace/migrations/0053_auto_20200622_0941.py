# Generated by Django 2.2 on 2020-06-22 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0052_job_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='commission',
            field=models.IntegerField(default=500),
        ),
    ]