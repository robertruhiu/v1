# Generated by Django 2.2 on 2020-10-15 08:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20200430_0917'),
        ('remote_codeln', '0002_auto_20201003_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_story', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('arbitration_required', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('amount', models.IntegerField(default=15)),
                ('due_date', models.DateTimeField()),
                ('escrow_disbursed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('stage', models.CharField(choices=[('backlog', 'Backlog'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='backlog', max_length=40)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.RemoteDeveloper')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.ProjectFeature')),
            ],
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
        migrations.RemoveField(
            model_name='escrowpayment',
            name='user',
        ),
        migrations.AddField(
            model_name='bid',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bid',
            name='budget',
            field=models.IntegerField(blank=True, default=15, null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='shortlisted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bid',
            name='timeline',
            field=models.DurationField(default=datetime.timedelta(days=14)),
        ),
        migrations.AddField(
            model_name='escrowpayment',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='remoteproject',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='remoteproject',
            name='posted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.RemoteProject'),
        ),
        migrations.AlterField(
            model_name='remoteproject',
            name='timeline',
            field=models.DurationField(default=datetime.timedelta(days=14)),
        ),
        migrations.AddField(
            model_name='remotedeveloper',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.RemoteProject'),
        ),
        migrations.AddField(
            model_name='projectfeature',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.RemoteDeveloper'),
        ),
        migrations.AddField(
            model_name='projectfeature',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.RemoteProject'),
        ),
        migrations.AddField(
            model_name='issue',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.ProjectFeature'),
        ),
        migrations.AddField(
            model_name='featurestory',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.ProjectFeature'),
        ),
        migrations.AddField(
            model_name='comments',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.Issue'),
        ),
        migrations.AddField(
            model_name='bid',
            name='developer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='remote_codeln.RemoteDeveloper'),
        ),
    ]