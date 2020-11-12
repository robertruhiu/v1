from django.db import models
from datetime import timedelta
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

# Create your models here.
from accounts.models import Profile


class RemoteProject(models.Model):
    PROJECT_TYPE = (
        ('website', 'Website'),
        ('android-App', 'Android App'),
        ('ios-App', 'Ios App'),
        ('desktop-App', 'Desktop Application'),
    )

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, max_length=200)
    tools = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client', blank=True, null=True)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project_type = models.CharField(max_length=40, choices=PROJECT_TYPE, default='website')
    team_size = models.CharField(max_length=20, choices=(
        ('single_dev', 'Single Developer'),
        ('team', 'Multiple Developers')), default='single_dev')
    budget = models.IntegerField(default=1000)
    designbudget = models.IntegerField(default=0)
    timeline = models.DurationField(default=timedelta(days=14))
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    stage =models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='developer', blank=True, null=True)
    verified = models.BooleanField(default=False)
    sign_date = models.DateTimeField(blank=True, null=True)


class RemoteDeveloper(models.Model):
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
class Signatures(models.Model):
    signature = models.TextField(blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)


class ProjectFeature(models.Model):
    name = models.CharField(max_length=120)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, max_length=200)
    amount = models.IntegerField(default=15)
    due_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(RemoteDeveloper, on_delete=models.CASCADE, blank=True, null=True)
    escrow_disbursed = models.BooleanField(default=False)
    stage = models.TextField(blank=True)
    developer_note = models.TextField(blank=True)



class FeatureStory(models.Model):
    feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
    user_story = models.TextField(blank=True)


class Tasks(models.Model):
    STAGE = (
        ('todo', 'Todo'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),

    )
    feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    stage = models.CharField(max_length=40, choices=STAGE, default='todo')
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)


class EscrowPayment(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=15)
    data = JSONField(default=dict)
    paid_at = models.DateTimeField(auto_now=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


class Bid(models.Model):
    budget = models.IntegerField(default=15, null=True, blank=True)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE, blank=True, null=True)
    timeline = models.DurationField(default=timedelta(days=14))
    tools = models.TextField(null=True, blank=True)
    shortlisted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    proposal = models.TextField(blank=True)
    withdraw = models.BooleanField(default=False)


class Issue(models.Model):
    feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
    title = models.CharField(max_length=120,default='myteam')
    description = models.TextField(blank=True)
    arbitration_required = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    tag = models.CharField(max_length=120,blank=True)



class Comments(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)

class Team(models.Model):
    name = models.CharField(max_length=120,default='myteam')
    lead = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    members = models.TextField(blank=True)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE, blank=True, null=True)
    pending = models.TextField(blank=True)

class Files(models.Model):
    description = models.TextField(blank=True)
    files = models.TextField(blank=True)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE, blank=True, null=True)

