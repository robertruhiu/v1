# Generated by Django 2.2 on 2020-03-27 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0076_auto_20200327_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Portfolio'),
        ),
    ]
