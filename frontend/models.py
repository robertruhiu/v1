from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from accounts.models import Profile
from marketplace.models import Job
from django_countries.fields import CountryField
from projects.models import Language, Framework ,Project
from transactions.models import Transaction
from separatedvaluesfield.models import SeparatedValuesField
from classroom.models import Subject
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

    def __str__(self):
        return f'{self.candidate} - {self.stage}'




class submissions(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    demo = models.CharField(null=True, max_length=400)
    repo = models.CharField(null=True, max_length=400)

    def __str__(self):
        return f'{self.candidate}'

class Portfolio(models.Model):
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='candidateportfolio')
    title = models.CharField(null=True, max_length=200)
    description = models.CharField(null=True, max_length=400)
    repository_link = models.CharField(null=True, max_length=400)
    demo_link = models.CharField(null=True, max_length=400)
    verified = models.BooleanField(default=False)
    tech_tags = models.CharField(max_length=500, blank=True, null=True, )
    csa = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.CharField(max_length=900, null=True, blank=True)
    dislikes = models.CharField(max_length=900, null=True, blank=True)
    search_vector = SearchVectorField(null=True)

    class Meta(object):
        indexes = [GinIndex(fields=['search_vector'])]

    def save(self, *args, **kwargs):
        # self.search_vector = (SearchVector('tech__tags'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.candidate}'


class Experience(models.Model):
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='candidateexperience')
    title = models.CharField(null=True, max_length=100)
    company = models.CharField(null=True, max_length=100)
    description = models.CharField(null=True, max_length=400)
    location = CountryField(null=True, max_length=30)
    duration = models.IntegerField(null=True)
    tech_tags = models.CharField(max_length=500, blank=True, null=True, )

    def __str__(self):
        return f'{self.candidate} - {self.title}'

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
    end_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
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
    csa = models.BooleanField(default=False)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True )
    workspace_link = models.URLField(blank=True, null=True)
    repo_link = models.URLField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.candidate} - {self.test_choice}'

class AssessmentReport(models.Model):
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    skill = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f'{self.candidate.user.first_name}: {self.project.name}'

class Cohort(models.Model):
    name = models.CharField(null=True, max_length=300)
    discord = models.CharField(null=True, max_length=300)
    members = models.CharField(null=True, max_length=800)
    created = models.DateTimeField(auto_now_add=True)

class Resources(models.Model):
    title = models.CharField(null=True, max_length=300)
    link = models.CharField(null=True, max_length=300)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    provider= models.CharField(max_length=300, null=True, blank=True)
    likes = models.CharField(max_length=900, null=True, blank=True)
    dislikes = models.CharField(max_length=900, null=True, blank=True)
    tags = models.CharField(max_length=300, null=True, blank=True)
    verified =models.BooleanField(default=False)