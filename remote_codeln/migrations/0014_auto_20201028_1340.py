# Generated by Django 2.2 on 2020-10-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_codeln', '0013_projectfeature_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='stage',
            field=models.CharField(choices=[('todo', 'Todo'), ('inprogress', 'In Progress'), ('done', 'Done')], default='todo', max_length=40),
        ),
    ]
