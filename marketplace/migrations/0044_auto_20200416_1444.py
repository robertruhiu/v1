# Generated by Django 2.2 on 2020-04-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0043_auto_20200221_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='rejectioncomment',
            field=models.CharField(max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='rejectionreason',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]
