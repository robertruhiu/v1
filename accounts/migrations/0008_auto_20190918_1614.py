# Generated by Django 2.2 on 2019-09-18 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='availabilty',
            field=models.CharField(choices=[('fulltime', 'fulltime'), ('contract', 'contract'), ('remote', 'remote'), ('parttime', 'parttime'), ('freelance', 'freelance')], max_length=30, null=True),
        ),
    ]