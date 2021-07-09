# Generated by Django 2.2.21 on 2021-06-30 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20210630_1047'),
        ('frontend', '0118_auto_20210630_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Portfolio'),
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=100, null=True)),
                ('course', models.CharField(max_length=100, null=True)),
                ('start_month', models.DateTimeField(blank=True, null=True)),
                ('end_month', models.DateTimeField(blank=True, null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidateeducation', to='accounts.Profile')),
            ],
        ),
    ]
