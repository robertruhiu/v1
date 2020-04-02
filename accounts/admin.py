from django.contrib import admin

# Register your models here.
from accounts.models import Profile, ReferralCode, Referral


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)


class ReferralCodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReferralCode, ReferralCodeAdmin)


class ReferralAdmin(admin.ModelAdmin):
    pass


admin.site.register(Referral, ReferralAdmin)
