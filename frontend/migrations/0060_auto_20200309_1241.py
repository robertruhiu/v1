# Generated by Django 2.2 on 2020-03-09 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0059_auto_20200309_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='dislikes',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='likes',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Portfolio'),
        ),
    ]