# Generated by Django 2.2 on 2020-01-06 17:24

from django.db import migrations, models
import django.db.models.deletion
import separatedvaluesfield.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0015_framework_image'),
        ('accounts', '0010_auto_20190927_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=500, null=True)),
                ('country', models.CharField(blank=True, max_length=400, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='EnterpriseDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('select_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnterpriseProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.Enterprise')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='EnterpriseDeveloperReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirements', separatedvaluesfield.models.SeparatedValuesField(blank=True, max_length=150, null=True)),
                ('competency', separatedvaluesfield.models.SeparatedValuesField(blank=True, max_length=150, null=True)),
                ('grading', separatedvaluesfield.models.SeparatedValuesField(blank=True, max_length=150, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('skill', models.CharField(blank=True, max_length=100, null=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='api.EnterpriseDeveloper')),
            ],
        ),
        migrations.AddField(
            model_name='enterprisedeveloper',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='api.EnterpriseProject'),
        ),
        migrations.CreateModel(
            name='EnterpriseAPIKey',
            fields=[
                ('id', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('prefix', models.CharField(editable=False, max_length=8, unique=True)),
                ('hashed_key', models.CharField(editable=False, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(default=None, help_text='A free-form name for the API key. Need not be unique. 50 characters max.', max_length=50)),
                ('revoked', models.BooleanField(blank=True, default=False, help_text='If the API key is revoked, clients cannot use it anymore. (This cannot be undone.)')),
                ('expiry_date', models.DateTimeField(blank=True, help_text='Once API key expires, clients cannot use it anymore.', null=True, verbose_name='Expires')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to='api.Enterprise')),
            ],
            options={
                'verbose_name': 'API key',
                'verbose_name_plural': 'API keys',
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
