import datetime

from decouple import config
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from api.models import EnterpriseAPIKey, EnterpriseProject, EnterpriseDeveloper
from api.serializers import EnterpriseDeveloperReport, \
    EnterpriseProjectSerializer, EnterpriseDeveloperReportSerializer


def setup_finished_mail(recipient, url):
    subject = 'Hi there your test is ready!'
    message = f'Your Workspace is ready.\n Go to {url} to start project'
    email_from = config('EMAIL_HOST_USER')
    request = [recipient]

    send_mail(subject, message, email_from, request)
    return HttpResponse('OK')


# Create your views here.

class EnterpriseProjects(generics.ListAPIView):
    serializer_class = EnterpriseProjectSerializer

    queryset = EnterpriseProject.objects.all()

    def list(self, request):
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise.projects
        # queryset = self.get_queryset()
        serializer = EnterpriseProjectSerializer(enterprise, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny,])
def schedule_test(request):
    if request.method == 'POST':
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise

        username = request.data.get('username')
        email = request.data.get('email')
        project_id = request.data.get('project_id')
        select_time = datetime.datetime.strptime(request.data.get('select_time'), '%Y-%m-%d %H:%M')
        project = EnterpriseProject.objects.get(pk=project_id)
        dev, created = EnterpriseDeveloper.objects.get_or_create(username=username, email=email, project=project)
        if created:
            dev.select_time = select_time
            dev.save()
            if dev.select_time.hour - datetime.datetime.now().hour < 3:
                url = f'https://{dev.username}-{project.slug}.codeln.com'
                setup_finished_mail(dev.email, url)
                return Response('You have successfully scheduled your test. A link will has been sent '
                                'to your inbox with the workspace and further instructions on how to proceed.')
            elif dev.select_time.hour - datetime.datetime.now().hour > 3:
                return Response('You have successfully scheduled your test. At the selected time a link will be sent '
                                'to your inbox with the workspace url and access and further instructions on how to '
                                'proceed.')
        else:
            # add job to poll for email
            dev.select_time = select_time
            dev.save()
            if  dev.select_time.hour - datetime.datetime.now().hour < 3:
                url = f'https://{dev.username}-{project.slug}.codeln.com'
                setup_finished_mail(dev.email, url)
                return Response('You have successfully updated your time. A link has been sent '
                                'to your inbox with the workspace and further instructions on how to proceed.')
            elif dev.select_time.hour - datetime.datetime.now().hour > 3 :
                return Response('You have successfully updated your time. At the selected time a link will be sent '
                                'to your inbox with the workspace url and access and further instructions on how to '
                                'proceed.')


# class ScheduleTest(APIView):
#     # queryset = EnterpriseProject.objects.all()
#
#     pass

#
# class EnterpriseReport(generics.RetrieveAPIView):
#     # permission_classes = [HasAPIKey]
#     serializer_class = EnterpriseDeveloperReport
#
#     def get(self, request):
#         key = request.headers.get('Api-Key')
#         key_prefix, _, _ = key.split('.')
#         enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
#         enterprise = enterprise_api_key.enterprise.projects
#
#         # queryset = self.get_queryset()
#         serializer = EnterpriseDeveloperReport(report)
#         return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny,])
def developer_report(request):
    if request.method == 'POST':
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise

        email = request.data.get('email')
        project_id = request.data.get('project_id')
        project = EnterpriseProject.objects.get(id=project_id)
        dev_report = EnterpriseDeveloperReport.objects.get(developer__email=email, developer__project=project)
        serializer = EnterpriseDeveloperReportSerializer(dev_report)
        return Response(serializer.data)


class AllReports(generics.ListAPIView):
    # permission_classes = [HasAPIKey]
    serializer_class = EnterpriseDeveloperReport
