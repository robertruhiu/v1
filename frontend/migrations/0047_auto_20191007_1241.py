# Generated by Django 2.2 on 2019-10-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0046_auto_20191007_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='frameworktested',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]