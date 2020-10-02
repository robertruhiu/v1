from django.db import models
from datetime import timedelta
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

# Create your models here.
# class ProjectFeature(models.Model):
#     name = models.CharField(max_length=120)
#     user_story = models.TextField(blank=True)
#     slug = models.SlugField(blank=True, max_length=200)
#     due_date = models.DateTimeField()
#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
#     paid = models.BooleanField(default=False)



class RemoteProject(models.Model):
    PROJECT_TYPE = (
        ('website', 'Website'),
        ('android-App', 'Android App'),
        ('ios-App', 'Ios App'),
        ('sesktop-App', 'Desktop Application'),
    )

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, max_length=200)
    project_type = models.CharField(max_length=40, choices=PROJECT_TYPE, default='website')
    team_size = models.CharField(max_length=20, choices=(
        ('single_dev', 'Single Developer'),
        ('team', 'Multiple Developers')), default='single_dev')
    budget = models.IntegerField(default=15)
    timeline = models.DurationField(default=timedelta(hours=2))
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


class EscrowPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=15)
    data = JSONField(default=dict)
    paid_at = models.DateTimeField(auto_now=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


# class FeatureComment(models.Model):
#     title = models.CharField(max_length=120)
#     feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
#     comment = models.TextField(blank=True)


