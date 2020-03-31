from django import forms

from feedback.models import RecruiterFeedback
    # DevFeedback, JobFeedback, RecruiterProductFeedback
#
#
# class DevFeedbackForm(forms.ModelForm):
#     class Meta:
#         model = DevFeedback
#         exclude = []
#
#
# class JobFeedbackForm(forms.ModelForm):
#     class Meta:
#         model = JobFeedback
#         exclude = []


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = RecruiterFeedback
        exclude = ['customer', 'job']
        # exclude = []
