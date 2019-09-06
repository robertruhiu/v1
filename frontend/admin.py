from django.contrib import admin

from frontend.models import Report, AssessmentReport, Assessment
# Register your models here.
class AssessmentReportAdmin(admin.ModelAdmin):
    pass

class AssessmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(AssessmentReport, AssessmentReportAdmin)
