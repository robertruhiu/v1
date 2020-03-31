from django.contrib import admin

from feedback.models import RecruiterFeedback, SurveyQuestion, Choice, SurveyAnswer


# Register your models here.

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(RecruiterFeedback)
class RecruiterFeedbackAdmin(admin.ModelAdmin):
    pass
