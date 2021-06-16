import datetime
import json

import pytz
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from marketplace.models import Job
from projects.forms import FrameworkForm
from projects.models import Project,Projecttype,Devtype,Framework
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import Projectserializer,FrameworkSerializer
from rest_framework import generics
import random
from django.contrib.auth.models import User
from marketplace.models import JobApplication,DevRequest
from accounts.models import Profile
from frontend.models import Assessment



class Projects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        job_id = self.kwargs['id']
        job = Job.objects.get(id=job_id)
        projects = Project.objects.all()
        tags = job.tech_stack.split(",")
        randomlist =[]
        for oneproject  in projects :
            for onetag in tags:
                if oneproject.tags.find(onetag.lower()):
                    randomlist.append(oneproject.id)

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]


        return Project.objects.filter(pk=projectid)

class RecommendedProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = User.objects.get(pk=user_id)
        userprofile = Profile.objects.get(user=user)
        projects = Project.objects.all()
        tags = userprofile.skills.split(",")


        randomlists =[]
        for oneproject  in projects :
            for onetag in tags:

                if onetag.lower() in oneproject.tags.lower():
                    randomlists.append(oneproject.id)
        randomlist = list(set(randomlists))

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]

        return Project.objects.filter(pk=projectid)

class BasicProject(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):


        user_id = self.kwargs['dev_id']
        user = Profile.objects.get(pk=user_id)
        # enable filter to ensure non repeat already done project in assessment
        doneprojects = Assessment.objects.filter(candidate=user)
        donelist =[]
        for onedoneproject in doneprojects:
            donelist.append(onedoneproject.project.id)

        projects = Project.objects.all()

        randomlists =[]
        for oneproject  in projects :
            if oneproject.level == 'Basic':
                randomlists.append(oneproject.id)


        randomlistinitial = list(set(randomlists))

        randomlist =list(set(randomlistinitial)-set(donelist))

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]

        return Project.objects.filter(pk=projectid)


class SelfverifyProject(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer

    def get_queryset(self):
        framework = self.kwargs['framework']
        user_id = self.kwargs['dev_id']
        user = Profile.objects.get(pk=user_id)
        # enable filter to ensure non repeat already done project in assessment
        doneprojects = Assessment.objects.filter(candidate=user)
        donelist = []
        for onedoneproject in doneprojects:
            donelist.append(onedoneproject.project.id)

        projects = Project.objects.all()
        randomlists = []
        for oneproject in projects:
            if oneproject.tags:
                if framework.lower() in oneproject.tags.lower():
                    randomlists.append(oneproject.id)

        randomlistinitial = list(set(randomlists))
        randomlist = list(set(randomlistinitial) - set(donelist))

        if len(randomlist) >= 1:
            projectid = random.choice(randomlist)
            projectid
            return Project.objects.filter(pk=projectid)
        else:
            return Project.objects.filter(pk=22)



class Allprojects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = Projectserializer

class ProjectDetails(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = Projectserializer

class RecentProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = Profile.objects.get(pk=user_id)
        recentprojects = JobApplication.objects.select_related('recruiter').filter(recruiter=user)
        project_ids = []
        for oneproject in recentprojects:
            if oneproject.project:
                project_ids.append(oneproject.project.id)
                return Project.objects.filter(pk__in=project_ids)

class MyRecentProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = Profile.objects.get(pk=user_id)
        recentprojects = DevRequest.objects.filter(owner=user)[:2]
        project_ids = []
        for oneproject in recentprojects:
            project_ids.append(oneproject.project)
        return project_ids

class Frameworks(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FrameworkSerializer
    queryset = Framework.objects.all()

# developer api views
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from frontend.models import AssessmentReport
from frontend.serializers import AssesmentReportSerializer, ClideAssesmentSerializer


class DeveloperProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        framework = self.kwargs['framework']

        developerprojects = Project.objects.filter(framework__name=framework)
        return developerprojects

# class DeveloperProjectReport(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get_object(self, candidate_id, project_id):
#         queryset = AssessmentReport.objects.filter(candidate=candidate_id).filter(project=project_id).get()
#         return queryset
#
#     def get(self, request, format=None):
#         candidate_id = request.GET.get('candidate_id')
#         project_id = request.GET.get('project_id')
#         report =  self.get_object(candidate_id, project_id)
#         serializer = AssesmentReportSerializer(report)
#         return Response(serializer.data)


# Create your views here.
# def project_categories(request):
#     # list all project categories
#     if request.method == 'GET':
#         return render(request, 'projects/categories.html', {})
#     elif request.method == 'POST':
#         return HttpResponse('<h2> Done </h2>')


# def project_category_list(request):
#     # list all project from above category
#     # filter projects by framework, language
#     pass

# class MultipleFieldLookupMixin(object):
#     """
#     Apply this mixin to any view or viewset to get multiple field filtering
#     based on a `lookup_fields` attribute, instead of the default single field filtering.
#     """
#     def get_object(self):
#         queryset = self.get_queryset()             # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             if self.kwargs[field]: # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         obj = get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj
#
# class DeveloperProjectReport(MultipleFieldLookupMixin, generics.RetrieveAPIView):
#     queryset = AssessmentReport.objects.all()
#     serializer_class = AssesmentReportSerializer
#     lookup_fields = ['candidate__id', 'project.id']

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def developerprojectreport(request, candidate_id, project_id):
    candidate = Profile.objects.get(id=candidate_id)
    project = Project.objects.get(id=project_id)
    candidate.verified_skills = project.tags
    candidate.save()
    report = AssessmentReport.objects.filter(candidate=candidate.user).filter(project=project).get()
    serializer = AssesmentReportSerializer(report)
    return Response(serializer.data)





@login_required
def project_list(request,type_id):
    # TODO: filter projects by framework, language and category using django filter
    categoryname=Projecttype.objects.get(id=type_id)

    projecttypes = Project.objects.filter(projecttype_id=type_id)
    return render(request, 'projects/all_projects.html', {'projecttypes': projecttypes,'categoryname':categoryname})
@login_required
def devtypes(request,dev_id):
    # TODO: filter projects by framework, language and category using django filter

    categoryname=Devtype.objects.get(id=dev_id)
    devtypes = Project.objects.filter(devtype_id=dev_id)
    return render(request, 'projects/devtypes.html', {'devtypes':devtypes,'categoryname':categoryname})
@login_required
def categories(request):
    projecttypes = Projecttype.objects.all()
    devtypes = Devtype.objects.all()

    return render(request, 'projects/categories.html',{'projecttypes':projecttypes, 'devtypes': devtypes})

@login_required
def project(request, id):

    frameworks =Framework.objects.all()
    project = Project.objects.get(id=id)
    framework_form = FrameworkForm()
    return render(request, 'projects/project.html', {'project': project,'frameworks':frameworks,
                                                     'framework_form':framework_form})

@api_view(['GET'])
@permission_classes((AllowAny,))
def clidext(request, email):
    dev = Profile.objects.get(user__email=email)
    tests = Assessment.objects.filter(candidate=dev, projectstarttime__date=datetime.datetime.now(tz=pytz.UTC).date(),
                                      completed=False)
    serializer = ClideAssesmentSerializer(tests, many=True)
    serializer
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((AllowAny,))
def clidextupdate(request, email,id):
    dev = Profile.objects.get(user__email=email)
    tests = Assessment.objects.get(id=id, candidate=dev)
    request
    if request.data != None:
        if request.data['livesharelink']:
          link = request.data['livesharelink']
          tests.workspace_link = link
          tests.save()
          return Response('Live Share link updated')
        elif request.data['repolink']:
            link = request.data['repolink']
            tests.repo_link = link
            tests.save()
            return Response('Repo saved!')
        elif request.data['completed']:
            tests.completed = True
            tests.save()
            return Response('Project Completed')
        else:
            return Response('Not a valid entry')
    else:
        return Response('No data submitted!')

