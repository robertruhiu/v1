from django.contrib import admin

from frontend.models import Report, AssessmentReport, Assessment, TestCenter
# Register your models here.
class AssessmentReportAdmin(admin.ModelAdmin):
    pass

class AssessmentAdmin(admin.ModelAdmin):
    pass

class TestCenterAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestCenter, TestCenterAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(AssessmentReport, AssessmentReportAdmin)
