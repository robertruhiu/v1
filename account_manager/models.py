
from django.db import models

# Create your models here.
from django.utils.text import slugify
from accounts.models import Profile


class Shortlist(models.Model):
    CATEGORY_CHOICES = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('mobile', 'Mobile'),
        ('java', 'Java'),
        ('python', 'Python'),
    )
    title = models.CharField(max_length=140)
    category = models.CharField(choices=CATEGORY_CHOICES, default='frontend', blank=True, max_length=100)
    developers = models.ManyToManyField(Profile, blank=True, related_name='dev_list')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        name = f'{self.title}-{self.category}'
        if self._state.adding:
            self.slug = slugify(name)
        super().save(*args, **kwargs)