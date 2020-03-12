import datetime
import json
import uuid

import pytz
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import Profile
from frontend.models import candidatesprojects, Assessment, TestCenter
from frontend.serializers import TestCenterSerializer
from servermanagement.forms import JobForm
from servermanagement.models import Job
from frontend.serializers import AssesmentSerializerUpdater
import datetime
# EnterpriseJob
# Create your views here.


class JobDetailView(generic.DetailView):
    model = Job


# def create_codeln_machine(request):
#     if request.method == 'POST':
#         codeln_machine_form = CodelnMachineCreateForm(request.POST)
#         if codeln_machine_form.is_valid():
#             codeln_machine_form.save()
#     else:
#         codeln_machine_form = CodelnMachineCreateForm()
#
#     return render(request, 'codeln_machine/create_machine.html', {'codeln_machine_form': codeln_machine_form})

# TODO: clean up
def test(request):
    server_config = ServerConfig.objects.get(type='ide_server_config')
    created_server_id = server_config.create_server('pm')
    server = Server.objects.create()
    return HttpResponse('ok')


# TODO: clean up
def test_widgets(request):
    return render(request, 'servermanagement/datepicker.html')


from decouple import config

DO_TOKEN = config('DO_TOKEN', default='DO_TOKEN')
DO_DOMAIN = config('DO_DOMAIN', default='DO_DOMAIN')
from servermanagement.models import Server, CandidateSetup, ServerConfig

do_headers = {'Content-Type': 'application/json',
              'Authentication': f"Bearer {DO_TOKEN}"}


def test_create_server(request=None):
    jobs = Job.objects.filter(has_executed=False,
                              type='create_server',
                              time__date=datetime.datetime.now(tz=pytz.UTC).date())

    for job in jobs:
        if datetime.datetime.now().hour - job.time.hour < 3:
            project_name = job.data['project_name']
            setup_code = job.data['setup_code']
            candidate_id = job.data['candidate_id']
            server_type = job.data['server_type']

            setup, created = CandidateSetup.objects.get_or_create(project_name=project_name, setup_code=setup_code,
                                                                  candidate_id=candidate_id, start_time=job.time,
                                                                  project=job.project)
            if created:
                print('reached server created Ist run')
                server_config = ServerConfig.objects.get(type=server_type)
                created_server_id, domain_name = server_config.create_server()
                Server.objects.create(machine_id=created_server_id, setup_code=setup_code,
                                      url=f'{domain_name}.{DO_DOMAIN}')
            else:
                print('reached server created 2nd run')
                server = Server.objects.get(setup_code=setup_code)
                if server.get_create_status():
                    server.assign_domain(server.url.split('.')[0])
                    job.has_executed = True
                    job.save()
                    Job.objects.create(type='create_workspace', project=job.project,
                                       data={'setup_code': job.data['setup_code'],
                                             'candidate_id': job.data['candidate_id']})
    return HttpResponse('Ok')


def report(request):
    candidate_setup = CandidateSetup.objects.filter(candidate_id=request.user.id).get()
    my_report = {}
    if candidate_setup.report != 'null':
        for metric_list in candidate_setup.report['component']['measures']:
            if metric_list['metric'] == 'quality_gate_details':
                new_value = json.loads(metric_list['value'])
                my_report[metric_list['metric']] = new_value['level']
            else:
                my_report[metric_list['metric']] = metric_list['value']
    return render(request, 'servermanagement/candidate_report.html', {'report': my_report,
                                                                      'candidate_setup': candidate_setup, })


def schedule_job(request, project_id):
    project = candidatesprojects.objects.get(id=project_id)
    if request.method == 'POST':
        job_form = JobForm(request.POST)
        my_data = {
            'project_id': project_id,
            'project_name': project.transaction.project.name,
            'candidate_id': request.user.id,
            'server_type': 'ide_server_config',
            'setup_code': str(uuid.uuid4())
        }
        try:
            # TODO: enforce user not set date before today
            day = request.POST['date']
            hour = request.POST['time']
            my_time = f'{day} {hour}'
            time_scheduled = datetime.datetime.strptime(my_time, '%Y-%m-%d %H:%M')
            timezone = pytz.UTC
            time_scheduled1 = timezone.localize(time_scheduled)
            if project.transaction.start_date.date() < time_scheduled1.date() < project.transaction.end_date.date():
                type = 'create_server'
                job = Job.objects.create(type=type, time=time_scheduled1,
                                         data=my_data, project=project)
                project.stage = 'time_set'
                project.save()
                # return redirect(reverse('jobs:job-detail', args=[job.pk]))
                return redirect(reverse('frontend:projectdetails', args=(project_id,)))
            else:
                # TODO:send user message to choose time between start date and end date
                return redirect(reverse('frontend:projectdetails', args=(project_id,)))
        except ValueError:
            # TODO:send message to user
            return redirect(reverse('frontend:projectdetails', args=(project_id,)))
        # # raise ValueError(f"invalid time, choose time between {project.transaction.start_date} and {
        # project.transaction.end_date}") try: # time_scheduled = pytz.utc.localize(datetime.datetime.combine(
        # job_form.cleaned_data.get('date'),job_form.cleaned_data.get('time'))) time_scheduled =
        # datetime.datetime.combine(job_form.cleaned_data.get('date'),job_form.cleaned_data.get('time')) if
        # time_scheduled > project.transaction.start_date and time_scheduled < project.transaction.end_date:
        #
        # except ValueError:
        #     raise ValueError("invalid time")
        # if job_form.is_valid():
        #     type = 'create_server'
        #     job = Job.objects.create(type=type, time=time_scheduled,
        #                              data=my_data, project=project)
        #     project.stage = 'time-set'
        #     project.save()
        #     # return redirect(reverse('jobs:job-detail', args=[job.pk]))
        #     return redirect(reverse('frontend:projectdetails', args=(project_id,)))
        # if job_form.is_valid():
        # return redirect(reverse('frontend:projectdetails', args=(project_id,)))


# Enterprise routing
# from transactions.models import EnterpriseCandidateProjects, EnterpriseProjects, EnterpriseCandidate, Enterprise, \
#     Candidate
# from transactions.serializers import EnterpriseProjectsSerializer, EnterpriseCandidateProjectsSerializer, \
#     EnterpriseCandidateSerializer
# from servermanagement.models import EnterpriseCandidateSetup
from django.http import Http404
from rest_framework.views import APIView

#  view that create test for enterprise users


# class EnterpriseCandidateDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return EnterpriseCandidate.objects.get(pk=pk)
#         except EnterpriseCandidate.DoesNotExist:
#             raise Http404
#
#     def get_enterprise(self, api_key):
#         try:
#             return Enterprise.objects.get(api_key=api_key)
#         except Enterprise.DoesNotExist:
#             raise Http404
#
# def post(self, request): data = request.data api_key = data.get('api_key') candidates = data.get('candidate_list')
# enterprise = self.get_enterprise(api_key=api_key) added_candidates = {} for candidate in candidates: fname =
# candidate['firstname'] lname = candidate['lastname'] email = candidate['email'] my_candid, created =
# Candidate.objects.get_or_create(first_name=fname, last_name=lname, email=email) my_ent_candid, exists_ =
# EnterpriseCandidate.objects.get_or_create(enterprise=enterprise, candidate=my_candid) added_candidates[
# my_ent_candid.id] = {"candidate_id": my_ent_candid.id, 'candidate_token': my_ent_candid.token,
# 'candidate_firstname': my_candid.first_name, 'candidate_lastname': my_candid.last_name, 'candidate_email':email} #
# return Response({"candidate_id": my_ent_candid.id, 'candidate_token': my_ent_candid.token}) return Response({
# 'addedcandidates': added_candidates})
#
# # view to send email to Candidates
# from servermanagement.email import enterprise_notification_mail
# class EnterpriseCandidateEmail(APIView):
#     def get_object(self, pk):
#         try:
#             return EnterpriseCandidate.objects.get(pk=pk)
#         except EnterpriseCandidate.DoesNotExist:
#             raise Http404
#
#     def get_enterprise(self, api_key):
#         try:
#             return Enterprise.objects.get(api_key=api_key)
#         except Enterprise.DoesNotExist:
#             raise Http404
#
#     def post(self, request):
#         data = request.data
#         api_key = data.get('api_key')
#         # candidates = data.get('candidate_list')
#         enterprise = self.get_enterprise(api_key=api_key)
#         allenterprisecandidates = EnterpriseCandidate.objects.filter(enterprise__id=enterprise.id)
#         for enterpisecandidate in allenterprisecandidates:
#             if not enterpisecandidate.invited:
#                 candidate = enterpisecandidate.candidate
#                 fname = candidate.first_name
#                 lname = candidate.last_name
#                 email = candidate.email
#                 token = enterpisecandidate.token
#                 enterprise_notification_mail(fname, lname, email, token)
#                 enterpisecandidate.invited = True
#                 enterpisecandidate.save()
#         return Response({'ok': 'ok'})
#
# class EnterpriseScheduleJob(APIView):
#     '''
#     create time from user event
#     '''
#
#     # TODO: filter by more than just the project id
#     def get_object(self, id):
#         try:
#             return EnterpriseCandidate.objects.get(id=id)
#         except EnterpriseCandidate.DoesNotExist:
#             raise Http404
#
#     # def get_project(self, name):
#     #     try:
#     #         return EnterpriseProjects.objects.get(project__name=name)
#     #     except EnterpriseProjects.DoesNotExist:
#     #         raise Http404
#
#     def post(self, request):
#         data = request.data
#         candidate = self.get_object(id=data.get('candidate_id'))
#         project = data.get('project_id')
#         token = data.get('candidate_token')
#
# # project = request.data.get('project') # candidate = data.get('candidate') my_data = { "project": project,
# 'project_name': project['name'], 'candidate': candidate.id, "server_type": "ide_server_config", "setup_code": str(
# uuid.uuid4()), "token": str(token), } try: # TODO: enforce user not set date before today day = data.get('date') #
#  hour = data.get('time') # my_time = f'{day} {hour}' time_scheduled = datetime.datetime.strptime(day,
#  '%Y-%m-%d %H:%M') timezone = pytz.UTC time_scheduled1 = timezone.localize(time_scheduled) # if
#  time_scheduled1.date() > my_project.project.start_date.date() and time_scheduled1.date() <
#  my_project.end_date.date(): type = 'create_server' choice_proj = Project.objects.get(name=project['name'])
#  new_project = EnterpriseProjects.objects.get(project_id=choice_proj.id) my_project, created =
#  EnterpriseCandidateProjects.objects.get_or_create(enterprise_candidate=candidate, enterprise_project=new_project)
#  job = EnterpriseJob.objects.create(type=type, time=time_scheduled1, project=my_project, data=my_data)
#  my_project.stage = 'time_set' my_project.save() return Response({"success": "Test successfully scheduled at
#  ".format(time_scheduled1)})
#
#         # TODO:send user message to choo se time between start date and end date
#         except Exception as e:
#             print(e.args[0])
#             # TODO: send message to user
#             return Response({"error": "Operation Failed"})
#
#
# class EnterpriseProjectsDetail(APIView):
#     '''
#     lists all enterprise projects
#     '''
#
#     def get_object(self, api_key):
#         # queryset = EnterpriseProjects.objects.all()
#         # api_key = self.kwargs['api_key']
#         queryset = EnterpriseProjects.objects.filter(enterprise__api_key=api_key)
#         return queryset
#
#     def get(self, request, format=None):
#         key = request.GET.get('api_key').strip()
#         list = self.get_object(key)
#         serializer = EnterpriseProjectsSerializer(list, many=True)
#         return Response(serializer.data)
#
#
# class EnterpriseCandidateProjectsDetail(APIView):
#     def get_object(self, api_key):
#         # queryset = EnterpriseProjects.objects.all()
#         # api_key = self.kwargs['api_key']
#
#         queryset = EnterpriseProjects.objects.filter(enterprise__api_key=api_key)
#         return queryset
#
#     def get(self, request, format=None):
#         key = request.GET.get('api_key').strip()
#         list = self.get_object(key)
#         serializer = EnterpriseCandidateProjectsSerializer(list, many=True)
#         return Response(serializer.data)
#
#
# class EnterpriseCandidateSetUpDetail(APIView):
#     def get_object(self, api_key):
#         # queryset = EnterpriseProjects.objects.all()
#         # api_key = self.kwargs['api_key']
#
#         queryset = EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)
#         return queryset
#
#     def get(self, request, format=None):
#         key = request.GET.get('api_key').strip()
#         filter_ = request.GET.get('filter_').strip()
#         if filter_ == 'in_progress':
#             pending = self.get_object(api_key=key).filter(project_completed=False)
#             serializer = EnterpriseCandidateSetupSerializer(pending, many=True)
#             return Response(serializer.data)
#         elif filter_ == 'completed':
#             completed = self.get_object(api_key=key).filter(project_completed=True)
#             serializer = EnterpriseCandidateSetupSerializer(completed, many=True)
#             return Response(serializer.data)
#         else:
#             my_list = self.get_object(key)
#             serializer = EnterpriseCandidateSetupSerializer(my_list, many=True)
#             return Response(serializer.data)
#     #
#     # def post(self, request):
#     #     pass

# class EnterpriseCandidateList(APIView):
#     def get_object(self, api_key):
#         # queryset = EnterpriseProjects.objects.all()
#         # api_key = self.kwargs['api_key']
#
#         queryset = EnterpriseCandidate.objects.filter(enterprise__api_key=api_key)
#         return queryset
#
#     def get(self, request, format=None):
#         key = request.GET.get('api_key').strip()
#         list = self.get_object(key)
#         serializer = EnterpriseCandidateSerializer(list, many=True)
#         return Response(serializer.data)
# def EnterpriseCandidateSetUpReport(APIView):
#     def get_candidate(self, token, api_key):
#         queryset = EnterpriseCandidateSetup.objects.get(project____token=token)
#         return queryset
#
#     def get_enterprise(self,api_key):
#         queryset = EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)
#         return queryset
#
#     def get(self, request, format=None):
#         api_key = request.GET.get('api_key').strip()
#         candidates =  self.get_enterprise(api_key=api_key)
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)
#
#
#     def post(self, request, format=None):
#         token = request.GET.get('token').strip()
#         candidate =  self.get_object(token)
#         serializer = EnterpriseCandidateSetupSerializer(candidate)
#         return Response(serializer.data)
#         # my_report = {}
#         # if serializer.data['report'] != 'null':
#         #     for metric_list in candidate.report['component']['measures']:
#         #         if metric_list['metric'] == 'quality_gate_details':
#         #             new_value = json.loads(metric_list['value'])
#         #             my_report[metric_list['metric']] = new_value['level']
#         #         else:
#         #             my_report[metric_list['metric']] = metric_list['value']
#         # return render(request, 'servermanagement/candidate_report.html', {'report': my_report,
#         #                                                       'candidate_setup': candidate_setup, })

from rest_framework import status, generics
# from servermanagement.models import Server

# class EnterpriseScheduleDemoJob(APIView):
#     '''
#     create time from user event
#     '''
#
#     # TODO: filter by more than just the project id
#     def get_object(self, id):
#         try:
#             return EnterpriseCandidate.objects.get(id=id)
#         except EnterpriseCandidate.DoesNotExist:
#             raise Http404
#
#
#     def post(self, request):
#         data = request.data
#         candidate = self.get_object(id=data.get('candidate_id'))
#         project = data.get('project_id')
#         token = data.get('candidate_token')
#         set_upcode = data.get('set_upcode')
#
#         # project = request.data.get('project')
#         # candidate = data.get('candidate')
#         my_data = {
#             "project": project,
#             'project_name': project['name'],
#             'candidate': candidate.id,
#             "server_type": "ide_server_config",
#             "setup_code": set_upcode,
#             "token": str(token),
#         }
#         try:
#             # TODO: enforce user not set date before today
#             day = data.get('date')
#             # hour = data.get('time')
#             # my_time = f'{day} {hour}'
#             time_scheduled = datetime.datetime.strptime(day, '%Y-%m-%d %H:%M')
#             timezone = pytz.UTC
#             time_scheduled1 = timezone.localize(time_scheduled)
#             # if time_scheduled1.date() > my_project.project.start_date.date() and time_scheduled1.date() < my_project.end_date.date():
#             type = 'create_server'
#             choice_proj = Project.objects.get(name=project['name'])
#             new_project = EnterpriseProjects.objects.get(project_id=choice_proj.id)
#             my_project, created = EnterpriseCandidateProjects.objects.get_or_create(enterprise_candidate=candidate,
#                                                                                     enterprise_project=new_project)
#             job = EnterpriseJob.objects.create(type=type, time=time_scheduled1, project=my_project, data=my_data)
#             server = Server.objects.get(setup_code=set_upcode)
#             workspace_url = f'http://{server.url}'
#             setup_finished_mail(candidate.candidate.email, workspace_url)
#             my_project.stage ='in_progress'
#             my_project.save()
#             return Response({"success": "Test successfully scheduled at ".format(time_scheduled1)})
#
#         # TODO:send user message to choose time between start date and end date
#         except Exception as e:
#             print(e.args[0])
#             # TODO: send message to user
#             return Response({"error": "Operation Failed"})
#
#
# @api_view(['GET'])
# def candidate_list(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates =  EnterpriseCandidate.objects.all().filter(enterprise__api_key=api_key)
#         serializer = EnterpriseCandidateSerializer(candidates, many=True)
#         return Response(serializer.data)
#
# @api_view(['GET']) def candidate_tested(request): api_key = request.GET.get('api_key') if request.method == 'GET':
# candidates =  EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)
# serializer = EnterpriseCandidateSetupSerializer(candidates, many=True) return Response(serializer.data)
#
# @api_view(['GET'])
# def candidate_pending(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates =  EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)\
#             .filter(project_completed=False)
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)
#
# @api_view(['GET'])
# def js_tested(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates = EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)\
#             .filter(project__enterprise_project__project__framework__language__name="Javascript")
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)
#
# @api_view(['GET'])
# def js_pending(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates =  EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)\
#             .filter(project__enterprise_project__project__framework__language__name= "Javascript").filter(project_completed=False)
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)
#
# @api_view(['GET'])
# def python_tested(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates =  EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)\
#             .filter(project__enterprise_project__project__framework__language__name="Python")
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)
#
# @api_view(['GET'])
# def python_pending(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates =  EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)\
#             .filter(project__enterprise_project__project__framework__language__name="Python").filter(project_completed=False)
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)\
#
# @api_view(['GET'])
# def allreports(request):
#     api_key = request.GET.get('api_key')
#     if request.method == 'GET':
#         candidates =  EnterpriseCandidateSetup.objects.filter(project__enterprise_project__enterprise__api_key=api_key)\
#             .filter(project_completed=True)
#         serializer = EnterpriseCandidateSetupSerializer(candidates, many=True)
#         return Response(serializer.data)
#
# def finish_project(request):
#     setup_code = request.GET.get('setup_code')
#     my_project = EnterpriseCandidateSetup.objects.get(setup_code=setup_code)
#     proj = my_project.project
#     proj.stage = "project_completed"

from servermanagement.models import Job
from servermanagement.serializers import AssesmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from servermanagement.email import manual_notification_mail, automated_notification_mail,\
    approve_candidate_mail, automated_test_chosen

class AssessmentJobCreate(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Assessment.objects.all()

    def get_object(self, id):
        asses = Assessment.objects.get(id=id)
        return asses

    def post(self, request):
        reqdata = request.data
        project = self.get_object(request.data.get('project_id'))
        # my_data = {
        #     'project_id': project.project.id,
        #     'project_name': project.project.name,
        #     'candidate_id': project.candidate.id,
        #     'server_type': 'ide_server_config',
        #     'setup_code': str(uuid.uuid4())
        # }
        # project = reqdata.get('project')
        setup_code = str(uuid.uuid4())
        type = 'create_server'
        time = reqdata.get('time')
        job = Job.objects.create(type=type, time=time, project=project, setup_code=setup_code)
        url1 = reverse('servermanagement:automated_test', args=(project.pk,))
        url2 = reverse('servermanagement:manual_test', args=(project.pk,))
        auto_url = "http://localhost:8000{}".format(url1)
        man_url = "http://localhost:8000{}".format(url2)
        approve_candidate_mail(project.candidate.full_name, project.candidate.country, project.projectstarttime,
                               project.candidate.user.email, auto_url, man_url)
        return Response('OK')

class AssessmentDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_assessment_object(self, pk):
        try:
            return Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        assessment = self.get_assessment_object(pk)
        serializer = AssesmentSerializer(assessment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        assessment = self.get_assessment_object(pk)
        serializer = AssesmentSerializer(assessment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        assessment = self.get_assessment_object(pk)
        assessment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# @permission_classes([AllowAny,])
# def manual_test(request, pk):
#     if request.method == 'GET':
#         assessment =  Assessment.objects.get(pk=pk)
#         assessment.test_mode = 'manual_test'
#         assessment.save()
#         # remove job model craeted
#         job = Job.objects.get(project=assessment, type='create_server')
#         job.delete()
#         # email to candidate
#         manual_notification_mail(assessment.candidate.user.email, assessment.projectstarttime)
#         return Response('OK')
#

class TestCenterList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TestCenter.objects.filter(start_time__gt=datetime.datetime.now())
    serializer_class = TestCenterSerializer

class manual_test(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Assessment.objects.all()
    serializer_class = AssesmentSerializerUpdater


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def manual_test1(request):
    if request.method == 'POST':
        candidate_id = request.data.get('candidate')
        test_center = request.data.get('test_center')
        frameworktested = request.data.get('frameworktested')
        candidate = Profile.objects.get(pk=candidate_id)
        test_center = TestCenter.objects.get(pk=test_center)
        assessment =  Assessment.objects.get_or_create(test_center=test_center, candidate=candidate,
                                                test_choice='on_site_test',frameworktested=frameworktested)
        return Response('OK')

@api_view(['GET'])
@permission_classes([AllowAny,])
def automated_test(request, pk):
    if request.method == 'GET':
        assessment =  Assessment.objects.get(pk=pk)
        assessment.stage = 'approved'
        assessment.test_mode = 'automated_test'
        assessment.save()
        # email to candidate
        automated_notification_mail(assessment.candidate.user.email, assessment.projectstarttime)
        automated_test_chosen('philisiah@codeln.com', assessment.candidate.full_name, assessment.projectstarttime,
                              assessment.project.name, assessment.frameworktested)
        return Response('OK')
