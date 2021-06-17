from django.contrib import admin

from frontend.models import Report, AssessmentReport, Assessment, TestCenter, Experience, submissions, Portfolio
# Register your models here.

@admin.register(AssessmentReport)
class AssessmentReportAdmin(admin.ModelAdmin):
    pass

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    raw_id_fields = ['portfolio', 'test_center', 'candidate', 'project', 'report']

    def get_ordering(self, request):
        return ['-projectstarttime']


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




