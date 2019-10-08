from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from accounts.models import Profile
from marketplace.models import Job
from django_countries.fields import CountryField
from projects.models import Language, Framework ,Project
from transactions.models import Transaction
from separatedvaluesfield.models import SeparatedValuesField

# Create your models here.
class candidatesprojects(models.Model):
    TYPE_CHOICES = (
        ('awaiting_candidate', 'Awaiting Candidate'),
        ('invite_accepted', 'Invite Accepted'),
        ('time_set', 'Time Set'),
        ('link_available', 'Link Available'),
        ('in_progress', 'In Progress'),
        ('project_completed', 'Project Completed'),
        ('analysis_started', 'Analysis Started'),
        ('transfer_complete', 'Transfer Complete'),
        ('analysis_complete', 'Analysis Complete'),
    )
    stage = models.CharField(max_length=100, default='awaiting_candidate', choices=TYPE_CHOICES)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE,null=True,)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,null=True,)




class submissions(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    demo = models.CharField(null=True, max_length=400)
    repo = models.CharField(null=True, max_length=400)

class Portfolio(models.Model):
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='candidateportfolio')
    title = models.CharField(null=True, max_length=200)
    description = models.CharField(null=True, max_length=400)
    repository_link = models.CharField(null=True, max_length=400)
    demo_link = models.CharField(null=True, max_length=400)
    verified = models.BooleanField(default=False)
    tech_tags = models.CharField(max_length=500, blank=True, null=True, )


class Experience(models.Model):
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='candidateexperience')
    title = models.CharField(null=True, max_length=100)
    company = models.CharField(null=True, max_length=100)
    description = models.CharField(null=True, max_length=400)
    location = CountryField(null=True, max_length=30)
    duration = models.IntegerField(null=True)
    tech_tags = models.CharField(max_length=500, blank=True, null=True, )

class Report(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    requirements= SeparatedValuesField(null=True,max_length=150,token=',')
    keycompitency = SeparatedValuesField(null=True,max_length=150,token=',')
    grading = SeparatedValuesField(null=True,max_length=150,token=',')
    score = models.IntegerField(null=True)
    github = models.CharField(null=True, max_length=300)

# temporary data model for demo
class TestCenter(models.Model):
    venue = models.CharField(blank=True,null=True,max_length=100)
    country = models.CharField(blank=True,null=True,max_length=100)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    location = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.venue} - {self.country} '

class Assessment(models.Model):
    STAGE_CHOICES = (
        ('invite_accepted', 'Invite Accepted'),
        ('time_set', 'Time Set'),
        ('link_available', 'Link Available'),
        ('in_progress', 'In Progress'),
        ('project_completed', 'Project Completed'),
        ('analysis_started', 'Analysis Started'),
        ('transfer_complete', 'Transfer Complete'),
        ('analysis_complete', 'Analysis Complete'),
    )
    TEST_CHOICES = (
        ('on_site_test', 'On Site Test'),
        ('automated_test', 'Automated Test'),
    )
    stage = models.CharField(choices=STAGE_CHOICES, default='invite_accepted', max_length=100, blank=True, null=True )
    test_choice = models.CharField(choices=TEST_CHOICES, default='automated_test', max_length=100)
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE,null=True, blank=True)
    projectstarttime = models.DateTimeField(null=True, blank=True)
    frameworktested = models.CharField(blank=True,null=True,max_length=500)
    demolink = models.CharField(blank=True,null=True,max_length=100)
    test_center = models.ForeignKey(TestCenter, on_delete=models.CASCADE, blank=True, null=True )

    def __str__(self):
        return f'{self.candidate.user.first_name} - {self.test_choice}'

class AssessmentReport(models.Model):
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    skill = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f'{self.candidate.user.first_name}: {self.project.name}'
