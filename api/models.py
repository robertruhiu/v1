from django.db import models
# Create your models here.
from rest_framework_api_key.models import AbstractAPIKey
from separatedvaluesfield.models import SeparatedValuesField

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
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tests')

    @property
    def developers(self):
        return self.developers.all()

    def __str__(self):
        return f'{self.enterprise.company_name} - {self.project.name} '


class EnterpriseDeveloper(models.Model):
    username = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    project = models.ForeignKey(EnterpriseProject, on_delete=models.CASCADE, related_name="developers")
    select_time = models.DateTimeField(null=True, blank=True)

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
