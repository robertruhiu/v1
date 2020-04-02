from django.urls import path

from feedback.views import dispatch_feedback_mail, recruiter_feedback

app_name = 'feedback'

urlpatterns = [
    path('dispatch_feedback_mail/', dispatch_feedback_mail, name='dispatch_feedback_mail'),
    # path('recruiter_feedback/', recruiter_feedback, name='recruiter_feedback'),
    path('rec/<slug:slug>/', recruiter_feedback, name='recruiter_feedback'),
]
