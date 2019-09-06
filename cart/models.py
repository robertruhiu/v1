from django.db import models

# Create your models here.
from accounts.models import Profile


class Cart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False)

    @property
    def total_amount(self):
        cost = [dev.price for dev in self.developerorder_set.all()]
        my_amount = sum(cost)
        amount = 0
        if len(cost) <= 10:
            amount = 200
        elif 11 >=len(cost) <=20:
            amount = 400
        return amount

    def __str__(self):
        return f'{self.user}'


class DeveloperOrder(models.Model):
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True)

    def set_price(self):
        self.price = 10
        return self.price

    def __str__(self):
        return f'{self.cart} - {self.developer}'
