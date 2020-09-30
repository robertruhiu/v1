from django.db import models

# Create your models here.
class ProjectFeature(models.Model):
    name = models.CharField(max_length=120)
    user_story = models.TextField(blank=True)
    slug = models.SlugField(blank=True, max_length=200)


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
    budget =models.IntegerField(default=15)
    timeline =
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)