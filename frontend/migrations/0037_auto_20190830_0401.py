# Generated by Django 2.2 on 2019-08-30 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0036_auto_20190829_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatesprojects',
            name='stage',
            field=models.CharField(choices=[('awaiting_candidate', 'Awaiting Candidate'), ('invite_accepted', 'Invite Accepted'), ('time_set', 'Time Set'), ('link_available', 'Link Available'), ('in_progress', 'In Progress'), ('project_completed', 'Project Completed'), ('analysis_started', 'Analysis Started'), ('transfer_complete', 'Transfer Complete'), ('analysis_complete', 'Analysis Complete')], default='awaiting_candidate', max_length=100),
        ),
    ]
