# Generated by Django 2.2 on 2019-08-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0038_auto_20190830_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='stage',
            field=models.CharField(choices=[('invite_accepted', 'Invite Accepted'), ('time_set', 'Time Set'), ('approved', 'Approved'), ('link_available', 'Link Available'), ('in_progress', 'In Progress'), ('project_completed', 'Project Completed'), ('analysis_started', 'Analysis Started'), ('transfer_complete', 'Transfer Complete'), ('analysis_complete', 'Analysis Complete')], default='invite_accepted', max_length=100),
        ),
    ]