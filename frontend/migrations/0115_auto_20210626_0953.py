# Generated by Django 2.2.21 on 2021-06-26 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0114_auto_20210614_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Portfolio'),
        ),
    ]
