from django.urls import path

from feedback.views import feedback_form, recruiter_feedback

app_name = 'feedback'

urlpatterns = [
    path('feedback/', feedback_form, name='feedback'),
    path('recruiter_feedback/', recruiter_feedback, name='recruiter_feedback'),
]
