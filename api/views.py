import datetime
import json

import pytz
import requests
from decouple import config
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import random_string_generator, IdeTemporalUser
from api.models import EnterpriseAPIKey, EnterpriseProject, EnterpriseDeveloper, WebHookSubscriber
from api.serializers import EnterpriseDeveloperReport, \
    EnterpriseProjectSerializer, EnterpriseDeveloperSerializer, \
    EnterpriseIntermediateProjectSerializer


def setup_finished_mail(dev_email, dev_password, dev_slug, ide_url, project_name, time_set):
    auth = (config('GOOD_TALENT_MJ_APIKEY_PUBLIC'), config('GOOD_TALENT_MJ_APIKEY_PRIVATE'))
    url = 'https://api.mailjet.com/v3.1/send'
    headers = {'Content-Type': 'application/json'}
    data = {"Messages": [
        {
            "From": {
                "Email": config('GOOD_TALENT_TEST_ADMIN'),
                "Name": "Good Talent Testing"
            },
            "To": [
                {
                    "Email": config('TEST_ADMIN'),
                    "Name": config('TEST_ADMIN_USER')
                }
            ],
            "Subject": "New Good Talent Assessment Scheduled",
            "TextPart": f"The following user : {dev_email} has scheduled a test at {time_set}\r\n "
                        f"for the project {project_name} and project_id is {dev_slug}"
                        f"The user password is {dev_password}\r\n "
                        f"Dev url is {ide_url}\r\n",
        }
    ]}
    req = requests.post(url=url, auth=auth, headers=headers, data=json.dumps(data))
    return HttpResponse('OK')


def setup_reschedule_mail(dev_email, dev_password, dev_slug, ide_url, project_name, time_set):
    auth = (config('GOOD_TALENT_MJ_APIKEY_PUBLIC'), config('GOOD_TALENT_MJ_APIKEY_PRIVATE'))
    url = 'https://api.mailjet.com/v3.1/send'
    headers = {'Content-Type': 'application/json'}
    data = {"Messages": [
        {
            "From": {
                "Email": config('GOOD_TALENT_TEST_ADMIN'),
                "Name": "Good Talent Testing"
            },
            "To": [
                {
                    "Email": config('TEST_ADMIN'),
                    "Name": config('TEST_ADMIN_USER')
                }
            ],
            "Subject": "Good Talent Assessment Rescheduled",
            "TextPart": f"The following user : {dev_email} has rescheduled a test to {time_set}\r\n "
                        f"for the project {project_name} and project_id is {dev_slug}"
                        f"The user password is {dev_password}\r\n "
                        f"Dev url is {ide_url}\r\n",
        }
    ]}
    req = requests.post(url=url, auth=auth, headers=headers, data=json.dumps(data))
    return HttpResponse('OK')


def goodtalent_mail(recipient, name, date):
    auth = (config('GOOD_TALENT_MJ_APIKEY_PUBLIC'), config('GOOD_TALENT_MJ_APIKEY_PRIVATE'))
    url = 'https://api.mailjet.com/v3.1/send'
    headers = {'Content-Type': 'application/json'}
    data = {"Messages": [
        {
            "From": {
                "Email": config('GOOD_TALENT_TEST_ADMIN'),
                "Name": "Good Talent Testing"
            },
            "To": [
                {
                    "Email": recipient,
                    "Name": name
                }
            ],
            "Bcc": [
                {
                    "Email": config('TEST_ADMIN')
                }
            ],
            "Subject": "Assessment Successfully Scheduled",
            "TextPart": f"Dear {name}, you have successfully scheduled an assessment on {date}.\r\n"
                        "15 minutes to the set time you will receive a link to your workspace in your inbox.\r\n"
                        "Feel free to reach out if you have any questions!!\r\n"
                        "Kind regards, Good Talent.\r\n",
        }
    ]}
    req = requests.post(url=url, auth=auth, headers=headers, data=json.dumps(data))
    return HttpResponse("Good talent email sent!")


def goodtalent_reschedule_mail(recipient, name, date):
    auth = (config('GOOD_TALENT_MJ_APIKEY_PUBLIC'), config('GOOD_TALENT_MJ_APIKEY_PRIVATE'))
    url = 'https://api.mailjet.com/v3.1/send'
    headers = {'Content-Type': 'application/json'}
    data = {"Messages": [
        {
            "From": {
                "Email": config('GOOD_TALENT_TEST_ADMIN'),
                "Name": "Good Talent Testing"
            },
            "To": [
                {
                    "Email": recipient,
                    "Name": name
                }
            ],
            "Bcc": [
                {
                    "Email": config('TEST_ADMIN')
                }
            ],
            "Subject": "Assessment Rescheduled",
            "TextPart": f"Dear {name}, you have successfully rescheduled an assessment to {date}.\r\n"
                        "15 minutes to the set time you will receive a link to your workspace in your inbox.\r\n"
                        "Feel free to reach out if you have any questions!!\r\n"
                        "Kind regards, Good Talent.\r\n",
        }
    ]}
    req = requests.post(url=url, auth=auth, headers=headers, data=json.dumps(data))
    return HttpResponse("Good talent email sent!")


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
@permission_classes([AllowAny, ])
def schedule_test(request):
    if request.method == 'POST':
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise

        username = request.data.get('username')
        email = request.data.get('email')
        project_id = request.data.get('project_id')
        metadata = request.data.get('metadata')
        date1 = datetime.datetime.strptime(request.data.get('select_time'), '%Y-%m-%d %H:%M')
        select_time = date1.replace(tzinfo=pytz.UTC)
        project = EnterpriseProject.objects.get(project_id=project_id)
        ide_password = random_string_generator(10)
        dev, created = EnterpriseDeveloper.objects.get_or_create(username=username, email=email, project=project)
        if created:
            temp_user = IdeTemporalUser.objects.create(username=username, email=email, password=ide_password)
            dev_password = temp_user.password
            dev.username = username
            dev.email = email
            dev.temp_user = temp_user
            dev.metadata = metadata
            dev.select_time = select_time
            dev.save()
            url = f'http://clide.goodtalent.dev?id={dev.slug}'
            if dev.select_time.hour - datetime.datetime.now().hour < 3:
                goodtalent_mail(dev.email, dev.username, dev.select_time)
                setup_finished_mail(dev.email, dev_password, dev.slug, url, project.project.name, dev.select_time)
                return Response('You have successfully scheduled your test. A link will has been sent '
                                'to your inbox with the workspace and further instructions on how to proceed.')
            elif dev.select_time.hour - datetime.datetime.now().hour > 3:
                goodtalent_mail(dev.email, dev.username, dev.select_time)
                setup_finished_mail(dev.email, dev_password, dev.slug, url, project.project.name, dev.select_time)
                return Response('You have successfully scheduled your test. At the selected time a link will be sent '
                                'to your inbox with the workspace url and access and further instructions on how to '
                                'proceed.')
        else:
            dev_password = dev.temp_user.password
            dev.select_time = select_time
            dev.save()
            url = f'http://demeide.goodtalent.dev?id={dev.slug}'
            if dev.select_time.hour - datetime.datetime.now().hour < 3:
                goodtalent_reschedule_mail(dev.email, dev.username, dev.select_time)
                setup_reschedule_mail(dev.email, dev_password, dev.slug, url, project.project.name, dev.select_time)
                return Response('You have successfully updated your time. A link has been sent '
                                'to your inbox with the workspace and further instructions on how to proceed.')
            elif dev.select_time.hour - datetime.datetime.now().hour > 3:
                goodtalent_reschedule_mail(dev.email, dev.username, dev.select_time)
                setup_reschedule_mail(dev.email, dev_password, dev.slug, url, project.project.name, dev.select_time)
                return Response('You have successfully updated your time. At the selected time a link will be sent '
                                'to your inbox with the workspace url and access and further instructions on how to '
                                'proceed.')


# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def scheduledtests(request):
#     if request.method == 'POST':
#         key = request.headers.get('Api-Key')
#         key_prefix, _, _ = key.split('.')
#         enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
#         enterprise = enterprise_api_key.enterprise
#
#         username = request.data.get('username')
#         email = request.data.get('email')
#         projects = EnterpriseDeveloper.objects.filter(username=username, email=email)
#
# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def taken_tests(request):
#     if request.method == 'POST':
#         key = request.headers.get('Api-Key')
#         key_prefix, _, _ = key.split('.')
#         enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
#         enterprise = enterprise_api_key.enterprise
#
#         username = request.data.get('username')
#         email = request.data.get('email')

class ScheduledTests(generics.ListAPIView):
    serializer_class = EnterpriseDeveloperSerializer

    queryset = EnterpriseDeveloper.objects.all()

    def list(self, request):
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise
        username = request.data.get('username')
        email = request.data.get('email')
        dev_projects = EnterpriseDeveloper.objects.filter(username=username, email=email, project_completed=False)
        # queryset = self.get_queryset()
        serializer = EnterpriseDeveloperSerializer(dev_projects, many=True)
        return Response(serializer.data)


class TakenTests(generics.ListAPIView):
    serializer_class = EnterpriseDeveloperSerializer

    queryset = EnterpriseDeveloper.objects.all()

    def list(self, request):
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise
        username = request.data.get('username')
        email = request.data.get('email')
        dev_projects = EnterpriseDeveloper.objects.filter(username=username, email=email, project_completed=True)
        # queryset = self.get_queryset()
        serializer = EnterpriseDeveloperSerializer(dev_projects, many=True)
        return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def developer_report(request):
#     if request.method == 'POST':
#         key = request.headers.get('Api-Key')
#         key_prefix, _, _ = key.split('.')
#         enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
#         enterprise = enterprise_api_key.enterprise
#
#         email = request.data.get('email')
#         project_id = request.data.get('project_id')
#         project = EnterpriseProject.objects.get(id=project_id)
#         dev_report = EnterpriseDeveloperReport.objects.get(developer__email=email, developer__project=project)
#         serializer = EnterpriseDeveloperReportSerializer(dev_report)
#         return Response(serializer.data)


class AllReports(generics.ListAPIView):
    # permission_classes = [HasAPIKey]
    serializer_class = EnterpriseDeveloperReport


# create a report function for demo purposes
@login_required
def create_report(slug):
    enterprisedev = EnterpriseDeveloper.objects.get(slug=slug)
    # requirements = request.data.get('requirements')
    # competency = request.data.get('competency')
    # grading = request.data.get('grading')
    # score = request.data.get('score')
    # skill = request.data.get('skill')

    requirements = {
        'Improved UI/UX': 'success',
        'Sign up for users at your Client\'s company': 'unsuccessful',
        'Login': 'success',
        'Persist the market data in a PostgreSQL database': 'success',
        'Allow users to set up alerts for a certain price point': 'unsuccessful',
    }
    grading = {
        'Tests Passed': 6,
        'Tests Failed': 6,
        'Warnings': 6,
        'Errors': 6,
        'Lines of Code': 216,
        'Duplications': '2%',
        'Classes': 6,
        'Comments': '5%',
        'Dependencies': 6,
        'Runtime': 3.45,
        'Technical Debt': 'nil',
        'Quality Gates': 'ok',
    }
    key_competencies = {
        'deliverables': '64%',
        'error_handling': '64%',
        'project_security': '64%',
        'code_readability': '64%',
        'time_used': '340 mins'

    }
    report = EnterpriseDeveloperReport.objects.create(requirements=requirements, competency=key_competencies,
                                                      grading=grading, developer=enterprisedev)
    return 'Report saved.'


# IDE should call this url when the developer is done with the project

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def enterprise_test_complete(request, slug):
    enterprisedeveloper = EnterpriseDeveloper.objects.get(slug=slug)
    enterprisedeveloper.project_completed = True
    time = datetime.datetime.now(tz=pytz.UTC)
    enterprisedeveloper.time_completed = time
    enterprisedeveloper.save()
    enterprise = enterprisedeveloper.project.enterprise
    url = WebHookSubscriber.objects.get(user=enterprise, webhook_event='on_test_complete').target_url
    payload = {
        "event": 'on_test_complete',
        "data": {
            'username': enterprisedeveloper.username,
            'email': enterprisedeveloper.email,
            'project_completed': enterprisedeveloper.project_completed,
            'metadata': enterprisedeveloper.metadata,
            'time_completed': str(enterprisedeveloper.time_completed),
        }
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    # create_report(slug)
    return Response('test_completed')


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def create_report(request, slug):
    enterprisedev = EnterpriseDeveloper.objects.get(slug=slug)
    # requirements = request.data.get('requirements')
    # competency = request.data.get('competency')
    # grading = request.data.get('grading')
    # score = request.data.get('score')
    # skill = request.data.get('skill')
    code_base = 'https://github.com/kamranahmedse/developer-roadmap.git'
    requirements = {
        'Improved UI/UX': 'success',
        'Sign up for users at your Client\'s company': 'unsuccessful',
        'Login': 'success',
        'Persist the market data in a PostgreSQL database': 'success',
        'Allow users to set up alerts for a certain price point': 'unsuccessful',
    }
    grading = {
        'Tests Passed': 6,
        'Tests Failed': 6,
        'Warnings': 6,
        'Errors': 6,
        'Lines of Code': 216,
        'Duplications': '2%',
        'Classes': 6,
        'Comments': '5%',
        'Dependencies': 6,
        'Runtime': 3.45,
        'Technical Debt': 'nil',
        'Quality Gates': 'ok',
    }
    key_competencies = {
        'deliverables': '64%',
        'error_handling': '64%',
        'project_security': '64%',
        'code_readability': '64%',
        'time_used': '340 mins'

    }
    report, created = EnterpriseDeveloperReport.objects.get_or_create(code_base=code_base, requirements=requirements,
                                                                      competency=key_competencies, grading=grading,
                                                                      developer=enterprisedev)
    return Response('Report saved.')


# IDE should call this url when the developer is done with the project has been analysed

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def enterprise_report_ready(request, slug):
    enterprisedev = EnterpriseDeveloper.objects.get(slug=slug)
    enterprisedevreport = EnterpriseDeveloperReport.objects.get(developer=enterprisedev)
    enterprisedevreport.report_ready = True
    time = datetime.datetime.now(tz=pytz.UTC)
    enterprisedevreport.time_completed = time
    enterprisedevreport.save()
    enterprise = enterprisedev.project.enterprise
    url = WebHookSubscriber.objects.get(user=enterprise, webhook_event='on_report_ready').target_url
    payload = {
        "event": 'on_report_ready',
        "data": {
            'code_base': enterprisedevreport.code_base,
            'requirements': enterprisedevreport.requirements,
            'competency': enterprisedevreport.competency,
            'grading': enterprisedevreport.grading,
            'score': enterprisedevreport.score,
            'metadata': enterprisedev.metadata,
            'time_completed': str(enterprisedevreport.time_completed),
        }
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    print(r.status_code)
    return Response('Report ready')

@login_required
def create_ide_user(request):
    from accounts.models import IdeTemporalUser
    IdeTemporalUser.objects.create(username='jerry', email='philisiah@codeln.com', password='Password007')


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_project(request, slug):
    project = EnterpriseDeveloper.objects.get(slug=slug).project.project
    project_data = EnterpriseIntermediateProjectSerializer(project).data
    return Response(project_data)
