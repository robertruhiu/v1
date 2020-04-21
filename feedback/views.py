from decouple import config
from django.core.mail import send_mail
from django.http import HttpResponse
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from feedback.models import RecruiterFeedback, SurveyAnswer
from feedback.serializers import RecruiterFeedbackSerializer


def feedback_email(email, slug, job):
    url = f'https://codeln.com/feedback/{slug}/'
    subject = f'Feedback on the {job}'
    message = f'Go to {url} to submit your feedback'
    email_from = config('EMAIL_HOST_USER')
    request = [email]

    send_mail(subject, message, email_from, request)
    return HttpResponse('OK')


def dispatch_feedback_mail(request):
    feedbacklist = RecruiterFeedback.objects.filter(submitted=False)
    for feedback in feedbacklist:
        feedback_email(feedback.customer.user.email, feedback.slug, feedback.job.title)
    return HttpResponse("emails sent")


# def recruiter_feedback(request, id):
#     recruiter = Profile.objects.get(id=id)
#     recruiter_feedback = RecruiterFeedback.objects.get(customer=recruiter)
#     selected_devs = JobApplication.objects.filter(recruiter=recruiter, job=recruiter_feedback.job, stage='active')
#     return render(request, 'feedback/email/recruitment_feedback.html',
#                   {'recruiter_feedback': recruiter_feedback, 'selected_devs': selected_devs})


# todo: change id to slug representing the feedback model
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def recruiter_feedback(request, slug):
    if request.method == 'GET':
        # recruiter = Profile.objects.get(id=1)
        recruiter_feedback = RecruiterFeedback.objects.get(slug=slug)
        recruiter_feedback_data = RecruiterFeedbackSerializer(recruiter_feedback).data
        return Response(recruiter_feedback_data)
    else:
        # recruiter = Profile.objects.get(id=1)
        recruiter_feedback = RecruiterFeedback.objects.get(slug=slug)

        for feedback in request.data:
            SurveyAnswer.objects.create(feedback_model=recruiter_feedback, question=feedback.question,
                                        text=feedback.text, developer=feedback.developer)
        content = {'message': 'feedback submitted'}
        return Response(content, status=status.HTTP_200_OK)
