import datetime
import random
import string

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django_countries.fields import CountryField
from separatedvaluesfield.models import SeparatedValuesField
from taggit.managers import TaggableManager


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('recruiter', 'RECRUITER'),
        ('developer', 'DEVELOPER'),
    )
    STAGE_CHOICES = (
        ('profile_type_selection', 'profile_type_selection'),
        ('recuiter_filling_details', 'recuiter_filling_details'),
        ('developer_filling_details', 'developer_filling_details'),
        ('complete', 'complete'),
    )
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )
    YEARS_ACTIVE_CHOICES = (
        ('0-1', '0-1'),
        ('1-2', '1-2'),
        ('2-4', '2-4'),
        ('4-above', '4-above'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, null=True, blank=True, max_length=30)
    stage = models.CharField(choices=STAGE_CHOICES, default='profile_type_selection', max_length=100)
    profile_photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    csa = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    student = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True, max_length=30)
    phone_number = models.CharField(null=True, max_length=30)
    # developer profile
    linkedin_url = models.CharField(max_length=500, null=True, )
    portfolio = models.CharField(max_length=500, blank=True, null=True)
    github_repo = models.CharField(max_length=500, null=True, )
    language = models.CharField(max_length=140, null=True, blank=True)
    framework = models.CharField(max_length=140, null=True, blank=True)
    years = models.CharField(choices=YEARS_ACTIVE_CHOICES, null=True, max_length=30)
    about = models.CharField(null=True, max_length=300)
    profile_tags = SeparatedValuesField(null=True, max_length=150, token=',')
    skills = models.CharField(max_length=900, null=True, blank=True)
    verified_skills = models.CharField(max_length=900, null=True, blank=True)
    country = CountryField(null=True, max_length=30)
    availabilty = models.CharField(null=True, max_length=100, blank=True)
    notifications = models.BooleanField(default=True)
    remote_entry = models.BooleanField(default=False)
    remote_verified = models.BooleanField(default=False)

    # years = models.CharField(max_length=30, choices=YEARS_ACTIVE_CHOICES, null=True, blank=True),

    # recruiter profile
    company = models.CharField(max_length=140, null=True, blank=True)
    job_role = models.CharField(max_length=140, null=True, blank=True)
    industry = models.CharField(max_length=80, null=True, blank=True)
    company_url = models.CharField(max_length=500, null=True, blank=True)
    tags = TaggableManager()
    file = CloudinaryField(resource_type="raw", blank=True)
    salary = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False

    def photo(self, default_path="default_user_photo.png"):
        if self.profile_photo:
            return self.profile_photo
        return default_path

    def get_absolute_url(self):
        return '/accounts/profile/'

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def date_joined(self):
        return self.user.date_joined

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Referral(models.Model):
    referrer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reffereds')
    referred = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='refferers')

    class Meta:
        unique_together = (('referrer', 'referred'),)

    def __str__(self):
        return f'{self.referrer} => {self.referred}'

    def clean(self, *args, **kwargs):
        if self.referrer == self.referred:
            raise ValidationError(('The referrer can not be referred.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Referral, self).save(*args, **kwargs)


class ReferralCode(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='referral_code')
    code = models.SlugField(default='', null=True, editable=False, unique=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f'{self.user.full_name} -> {str(self.code)}'

    def save(self, *args, **kwargs):
        if not self.code:
            strval = random_string_generator(4).upper()
            name = self.user.user.username[:3].upper()
            value = f'{name}{strval}'
            self.code = slugify(value, allow_unicode=True)
        return super().save(*args, **kwargs)


class IdeTemporalUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self._state.adding:
            username = self.username
            if User.objects.filter(username=self.username).exists():
                username += str(random.choice(range(1000)))
                self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}-{self.password}'


@receiver(post_save, sender=IdeTemporalUser)
def create_ide_user(sender, instance, created, **kwargs):
    if created:
        new_ide_user = User.objects.create_user(username=instance.username, email=instance.email, password=instance.password)
        instance.user = new_ide_user
        instance.save()
    pass


@receiver(post_delete, sender=IdeTemporalUser)
def delete_ide_user(sender, instance, **kwargs):
    instance.user.delete()

