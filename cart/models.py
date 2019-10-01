from django.db import models

# Create your models here.
from accounts.models import Profile


class Cart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False)
    devspending = models.CharField(max_length=900, null=True, blank=True)
    devspaid = models.CharField(max_length=900, null=True, blank=True)
    amount = models.IntegerField(blank=True,default=0)
    transaction_id = models.CharField(max_length=900, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    conditions = models.BooleanField(default=False)




