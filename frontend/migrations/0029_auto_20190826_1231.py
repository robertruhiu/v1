# Generated by Django 2.2 on 2019-08-26 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0028_auto_20190826_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Report'),
        ),
    ]
