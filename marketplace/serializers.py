from django.contrib.auth.models import User
from marketplace.models import DevRequest,Job,JobApplication,Job,DeveloperReport
from rest_framework import serializers
from frontend.serializers import ProfileSerializer,ReportSerializer
from projects.serializers import Projectserializer
from projects.models import Project


class DeveloperReportSerilizer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperReport
        fields = '__all__'

class DeveloperReportCreatorSerilizer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperReport
        fields = ['id','score']
class DevRequestSerializer(serializers.ModelSerializer):
    developer = ProfileSerializer()
    owner = ProfileSerializer()
    project = Projectserializer()
    report = DeveloperReportSerilizer()
    class Meta:
        model = DevRequest
        fields = ['id','developer', 'paid', 'stage', 'interviewstarttime', 'interviewendtime', 'notes',
                  'owner', 'test_stage', 'project',
                  'report', 'interviewstatus', 'eventcolor','projectstarttime','offerstatus','offerletter','demolink','notes' ]
class DevRequestSerializersimple(serializers.ModelSerializer):
    developer = ProfileSerializer
    owner = ProfileSerializer
    project = Projectserializer
    report = DeveloperReportSerilizer
    class Meta:
        model = DevRequest
        fields = ['id','developer', 'paid', 'stage', 'interviewstarttime', 'interviewendtime', 'notes',
                  'owner', 'test_stage', 'project',
                  'report', 'interviewstatus', 'eventcolor','projectstarttime','offerstatus','offerletter','demolink','notes' ]
class DevRequestUpdaterSerializer(serializers.ModelSerializer):
    developer = ProfileSerializer
    owner = ProfileSerializer
    project = Projectserializer
    report = DeveloperReportSerilizer
    class Meta:
        model = DevRequest
        fields = ['id','developer', 'paid', 'stage', 'interviewstarttime', 'interviewendtime', 'notes',
                  'owner', 'test_stage', 'project',
                  'report', 'interviewstatus', 'eventcolor','projectstarttime','offerstatus','offerletter','demolink','notes' ]

class JobRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'


class JobApplicationsRequestSerializer(serializers.ModelSerializer):
    job = JobRequestSerializer()
    candidate = ProfileSerializer()
    recruiter = ProfileSerializer()
    project = Projectserializer()
    report = DeveloperReportSerilizer()

    class Meta:
        model = JobApplication
        fields = ['id','job','candidate','selected','stage','interviewstarttime','interviewendtime',
                  'notes','recruiter','test_stage','project',
                  'report','interviewstatus','eventcolor','projectstarttime','offerstatus','offerletter',
                  'demolink','carted','type','framework','teststarttime','testendtime','notes','rejectionreason','rejectioncomment']
class JobApplicationsRequestSerializerspecific(serializers.ModelSerializer):
    job = JobRequestSerializer
    candidate = ProfileSerializer()
    recruiter = ProfileSerializer
    project = Projectserializer()
    report = DeveloperReportSerilizer()

    class Meta:
        model = JobApplication
        fields = ['id','job','candidate','selected','stage','interviewstarttime','interviewendtime',
                  'notes','recruiter','test_stage','project',
                  'report','interviewstatus','eventcolor','projectstarttime','offerstatus',
                  'offerletter','demolink','carted','type','framework','teststarttime','testendtime','notes','rejectionreason','rejectioncomment','created']

class MyapplicantsRequestSerializer(serializers.ModelSerializer):
    job = JobRequestSerializer
    candidate = ProfileSerializer
    recruiter = ProfileSerializer
    project = Projectserializer
    report = DeveloperReportSerilizer

    class Meta:
        model = JobApplication
        fields = ['id','job','candidate','selected','stage','interviewstarttime','interviewendtime',
                  'notes','recruiter','test_stage','project',
                  'report','interviewstatus','eventcolor','projectstarttime','offerstatus',
                  'offerletter','demolink','carted','type','framework','teststarttime','testendtime','rejectionreason','rejectioncomment']
class MyapplicantsRequestSerializersliced(serializers.ModelSerializer):
    job = JobRequestSerializer
    candidate = ProfileSerializer
    recruiter = ProfileSerializer
    project = Projectserializer
    report = DeveloperReportSerilizer

    class Meta:
        model = JobApplication
        fields = ['id','job','candidate','selected','stage','interviewstarttime','interviewendtime',
                  'notes','recruiter','test_stage','project',
                  'report','interviewstatus','eventcolor','projectstarttime','offerstatus','offerletter','demolink',
                  'carted','type''framework','teststarttime','testendtime','notes','rejectionreason','rejectioncomment']


class JobApplicationsUpdaterSerializer(serializers.ModelSerializer):
    job = JobRequestSerializer
    candidate = ProfileSerializer
    recruiter = ProfileSerializer
    project = Projectserializer
    report = DeveloperReportSerilizer


    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'candidate', 'selected', 'stage', 'interviewstarttime', 'interviewendtime',
                  'notes', 'recruiter', 'test_stage', 'project',
                  'report', 'interviewstatus', 'eventcolor','projectstarttime','offerstatus',
                  'offerletter','demolink','carted','type','framework','teststarttime','testendtime','notes','rejectionreason','rejectioncomment']



