# Generated by Django 2.0.4 on 2018-12-10 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0031_auto_20181210_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='answer',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='classroom.Answer'),
        ),
    ]
