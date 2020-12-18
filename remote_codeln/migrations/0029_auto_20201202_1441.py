# Generated by Django 2.2 on 2020-12-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20200430_0917'),
        ('remote_codeln', '0028_merge_20201125_0628'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comments',
        ),
        migrations.AlterField(
            model_name='remoteproject',
            name='project_type',
            field=models.CharField(choices=[('website', 'Website'), ('android-App', 'Android App'), ('ios-App', 'Ios App'), ('desktop-App', 'Desktop Application')], default='website', max_length=40),
        ),
    ]
