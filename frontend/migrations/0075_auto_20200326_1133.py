# Generated by Django 2.2 on 2020-03-26 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0074_auto_20200326_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Portfolio'),
        ),
    ]