# Generated by Django 2.2 on 2020-11-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_codeln', '0026_signatures'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remoteproject',
            name='client_sign',
        ),
        migrations.RemoveField(
            model_name='remoteproject',
            name='developer_sign',
        ),
        migrations.AddField(
            model_name='remoteproject',
            name='sign_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
