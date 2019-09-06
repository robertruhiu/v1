# Generated by Django 2.2 on 2019-09-01 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0040_assessment_manualtest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='manualtest',
        ),
        migrations.AddField(
            model_name='assessment',
            name='test_mode',
            field=models.CharField(choices=[('pending', 'Pending'), ('manual_test', 'Manual Test'), ('automated_test', 'Automated Test')], default='pending', max_length=100),
        ),
    ]