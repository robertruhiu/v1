from django.contrib import admin

from frontend.models import AssessmentReport
# Register your models here.
class AssessmentReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(AssessmentReport, AssessmentReportAdmin)