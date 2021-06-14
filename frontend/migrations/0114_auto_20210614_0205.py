# Generated by Django 2.2.21 on 2021-06-14 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0113_auto_20210526_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assessment',
            name='repo_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='workspace_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Portfolio'),
        ),
    ]
