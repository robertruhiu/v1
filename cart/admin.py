from django.contrib import admin

# Register your models here.

# Register your models here.
from cart.models import Cart, DeveloperOrder


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(DeveloperOrder)
class DeveloperOrderAdmin(admin.ModelAdmin):
    pass