# Generated by Django 2.2.21 on 2021-06-28 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_organizationinvitation'),
        ('marketplace', '0060_auto_20210626_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization'),
        ),
    ]
