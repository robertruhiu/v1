from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import Profile
from feedback.forms import FeedbackForm
from feedback.models import RecruiterFeedback
from feedback.serializers import RecruiterFeedbackSerializer


def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('response sent')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})


# def recruiter_feedback(request, id):
#     recruiter = Profile.objects.get(id=id)
#     recruiter_feedback = RecruiterFeedback.objects.get(customer=recruiter)
#     selected_devs = JobApplication.objects.filter(recruiter=recruiter, job=recruiter_feedback.job, stage='active')
#     return render(request, 'feedback/email/recruitment_feedback.html',
#                   {'recruiter_feedback': recruiter_feedback, 'selected_devs': selected_devs})


# todo: change id to slug representing the feedback model
@api_view(['GET', 'POST'])
@permission_classes([AllowAny, ])
def recruiter_feedback(request):
    if request.method == 'GET':
        recruiter = Profile.objects.get(id=1)
        recruiter_feedback = RecruiterFeedback.objects.get(customer=recruiter)
        recruiter_feedback_data = RecruiterFeedbackSerializer(recruiter_feedback).data
        return Response(recruiter_feedback_data)
    else:
        print(request.data)
        content = {'message': 'feedback submitted'}
        return Response(content, status=status.HTTP_200_OK)