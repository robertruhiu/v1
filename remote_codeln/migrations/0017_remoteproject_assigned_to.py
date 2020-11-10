# Generated by Django 2.2 on 2020-10-30 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20200430_0917'),
        ('remote_codeln', '0016_issue_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='remoteproject',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='developer', to='accounts.Profile'),
        ),
    ]