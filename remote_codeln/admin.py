from django.contrib import admin

# Register your models here.

from remote_codeln.models import RemoteProject, EscrowPayment, Bid

@admin.register(RemoteProject)
class RemoteProject(admin.ModelAdmin):
    pass

@admin.register(EscrowPayment)
class EscrowPaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass