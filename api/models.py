from datetime import datetime, timezone

import pytz
from django.db import models
# Create your models here.
from django.utils.text import slugify
from rest_framework_api_key.models import AbstractAPIKey
from separatedvaluesfield.models import SeparatedValuesField
from django.contrib.postgres.fields import JSONField


from accounts.models import Profile
from projects.models import Project


class Enterprise(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=400, null=True, blank=True)

    @property
    def projects(self):
        return self.projects.all()

    def __str__(self):
        return f'{self.user.full_name} - {self.company_name}'


class EnterpriseAPIKey(AbstractAPIKey):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="api_keys", )

    def __str__(self):
        return f'{self.enterprise}'


class EnterpriseProject(models.Model):
    slug = models.SlugField(default='', editable=False, null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tests')

    @property
    def developers(self):
        return self.developers.all()

    def save(self, *args, **kwargs):
        value = self.project.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.enterprise.company_name} - {self.slug} '



class EnterpriseDeveloper(models.Model):
    username = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    project = models.ForeignKey(EnterpriseProject, on_delete=models.CASCADE, related_name="developers")
    select_time = models.DateTimeField(null=True, blank=True)
    project_completed = models.BooleanField(default=False)
    time_completed = models.DateTimeField(null=True, blank=True)
    metadata = JSONField(null=True, blank=True)

    @property
    def report(self):
        return self.report.all()

    def __str__(self):
        return f'{self.username} - {self.email} '


class EnterpriseDeveloperReport(models.Model):
    requirements = SeparatedValuesField(null=True, max_length=150, token=',', blank=True)
    competency = SeparatedValuesField(null=True, max_length=150, token=',', blank=True)
    grading = SeparatedValuesField(null=True, max_length=150, token=',', blank=True)
    score = models.IntegerField(null=True, blank=True)
    skill = models.CharField(blank=True, null=True, max_length=100)
    developer = models.ForeignKey(EnterpriseDeveloper, on_delete=models.CASCADE, related_name="report")
    report_ready = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.developer.project.project.name} - {self.developer.username}'


class WebHookSubscriber(models.Model):

    WEBHOOK_EVENTS_CHOICES = (
        ('on_test_complete', 'Test Complete'),
        ('on_report_ready', 'Report Ready'),
    )
    user = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    target_url = models.URLField()
    webhook_event = models.CharField(max_length=140, default='test_complete', choices=WEBHOOK_EVENTS_CHOICES,
                                     null=True, blank=True)

    def __str__(self):
        return f'{self.webhook_event} -> {self.target_url}'
