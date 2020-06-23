from django.contrib import admin

from marketplace.models import Job, JobApplication, DevRequest,DeveloperReport


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(DevRequest)
class DevRequestAdmin(admin.ModelAdmin):
    pass
@admin.register(DeveloperReport)
class DeveloperReportAdmin(admin.ModelAdmin):
    pass