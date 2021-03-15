from django.contrib import admin

from frontend.models import Report, AssessmentReport, Assessment, TestCenter, Experience, submissions, Portfolio
# Register your models here.

@admin.register(AssessmentReport)
class AssessmentReportAdmin(admin.ModelAdmin):
    pass

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    pass

@admin.register(TestCenter)
class TestCenterAdmin(admin.ModelAdmin):
    pass

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    pass

@admin.register(submissions)
class SubmissionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Portfolio)
class Portfolio(admin.ModelAdmin):
    pass


