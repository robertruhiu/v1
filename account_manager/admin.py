from django.contrib import admin

# Register your models here.
from account_manager.models import Shortlist


@admin.register(Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    raw_id_fields = ['developers']