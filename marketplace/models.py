import json

from django.contrib.postgres.search import SearchVectorField, SearchVector

from account_manager.managers import JobManager
from accounts.models import Profile
from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from separatedvaluesfield.models import SeparatedValuesField
import uuid
from projects.models import Project
from django.contrib.postgres.fields import JSONField


class Job(models.Model):
    ENGAGEMENT_TYPE = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
        ('Freelance', 'Freelance'),
    )

    JOB_ROLE = (
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend  Developer', 'Backend  Developer'),
        ('Android  Developer', 'Android  Developer'),
        ('Graphic Designer', 'Graphic Designer'),
        ('IOS Developer', 'IOS Developer'),
        ('Data Scientist', 'Data Scientist'),
    )

    DEV_EXPERIENCE = (
        ('Entry', 'Entry'),
        ('Junior', 'Junior'),
        ('Mid-Level', 'Mid-Level'),
        ('Senior', 'Senior'),
    )
    YEARS_ACTIVE_CHOICES = (
        ('0-1', '0-1'),
        ('1-3', '1-3'),
        ('3-above', '3-above'),
    )
    company = models.CharField(max_length=300,null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True, blank=True)
    city = models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    job_role = models.CharField(max_length=30, choices=JOB_ROLE, default='Full Stack Developer')
    dev_experience = models.CharField(max_length=30, choices=DEV_EXPERIENCE, default='Mid-Level')
    engagement_type = models.CharField(max_length=30, choices=ENGAGEMENT_TYPE, default='Full-time')
    tech_stack = models.CharField(max_length=500,null=True, blank=True)
    num_devs_wanted = models.IntegerField(default=1)
    location = CountryField(null=True, max_length=30)
    remuneration = models.CharField(max_length=45, help_text='in dollars ($)',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    position_filled = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    commission = models.IntegerField(default=500)
    years_experience= models.CharField(max_length=30, choices=YEARS_ACTIVE_CHOICES, default='1-3')
    transaction_id = models.CharField(max_length=900, null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = JobManager()

    def save(self, *args, **kwargs):
        # self.search_vector = (SearchVector('company', 'title', 'job_role', 'tech_stack', 'city'))
        super().save(*args, **kwargs)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

class DeveloperReport(models.Model):
    code_base = models.URLField(null=True, blank=True)
    requirements = JSONField(null=True,  blank=True)
    competency = JSONField(null=True,  blank=True)
    grading = JSONField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    skill = models.CharField(blank=True, null=True, max_length=100)
    report_ready = models.BooleanField(default=False)

class JobApplication(models.Model):
    job = models.ForeignKey(Job, related_name='job_applications', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='devs')
    recruiter = models.ForeignKey(Profile, related_name='jobrecruiter', on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    report = models.ForeignKey(DeveloperReport, on_delete=models.CASCADE, null=True, blank=True)
    stage = models.CharField(max_length=500, null=True)
    interviewstarttime = models.DateTimeField(null=True,blank=True)
    interviewendtime = models.DateTimeField(null=True, blank=True)
    notes =  models.TextField(null=True, blank=True)
    test_stage = models.CharField(max_length=500, null=True)
    interviewstatus = models.CharField(max_length=500, null=True)
    eventcolor = models.CharField(max_length=100, null=True,default='blue')
    projectstarttime = models.DateTimeField(null=True, blank=True)
    offerstatus = models.CharField(max_length=500, null=True)
    offerletter = models.CharField(max_length=500, null=True)
    demolink = models.CharField(blank=True, null=True, max_length=100)
    type=models.CharField(max_length=500, null=True,default='applied')
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    framework = models.CharField(max_length=500, null=True)
    teststarttime = models.DateTimeField(null=True, blank=True)
    testendtime = models.DateTimeField(null=True, blank=True)
    rejectionreason=models.CharField(max_length=1500,null=True,blank=True)
    rejectioncomment=models.CharField(max_length=1500,null=True, blank=True)
    relevance = models.IntegerField(default=0)
    selected = models.BooleanField(default=False)
    carted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.candidate} - {self.job}'



class DevRequest(models.Model):
    owner = models.ForeignKey(Profile, related_name='owner', on_delete=models.CASCADE)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='devaccount',null=True,)
    paid = models.BooleanField(default=False)
    stage = models.CharField(max_length=500, null=True)
    interviewstarttime = models.DateTimeField(null=True, blank=True)
    interviewendtime = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=1500, null=True)
    test_stage = models.CharField(max_length=500, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    report = models.ForeignKey(DeveloperReport, on_delete=models.CASCADE,null=True, blank=True)
    interviewstatus = models.CharField(max_length=500, null=True)
    eventcolor = models.CharField(max_length=100, null=True, default='blue')
    projectstarttime = models.DateTimeField(null=True, blank=True)
    offerstatus = models.CharField(max_length=500, null=True)
    offerletter = models.CharField(max_length=500, null=True)
    demolink = models.CharField(blank=True, null=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)








