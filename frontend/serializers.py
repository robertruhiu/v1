from django.contrib.auth.models import User
from django_countries import Countries
from rest_framework import serializers

from accounts.models import Profile
from frontend.models import Experience, Portfolio, candidatesprojects, AssessmentReport, Assessment, Report, TestCenter,Resources,Cohort
from projects.serializers import Projectserializer as MainProjectSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                 'username','date_joined','is_staff')

class SerializableCountryField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super(SerializableCountryField, self).__init__(choices=Countries())

    def to_representation(self, value):
        if value in ('', None):
            return ''  # normally here it would return value. which is Country(u'') and not serialiable
        return super(SerializableCountryField, self).to_representation(value)

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    country = SerializableCountryField(allow_blank=True)

    class Meta:
        model = Profile
        fields = ('id','user','user_type','stage','csa','gender','linkedin_url','github_repo',
                  'years','about','skills','verified_skills',
                  'country','availabilty','company','job_role','industry','company_url','file','salary','available','student','notifications')

class ProfileSerializerUpdater(serializers.ModelSerializer):
    user = UserSerializer
    country = SerializableCountryField(allow_blank=True)

    class Meta:
        model = Profile
        fields = ('id','user','user_type','stage','csa','gender','linkedin_url','github_repo',
                  'years','about','skills','verified_skills',
                  'country','availabilty','company','job_role','industry','company_url','file','salary','available','student','notifications')


class ExperienceSerializer(serializers.ModelSerializer):
    candidate = ProfileSerializer()
    location = SerializableCountryField(allow_blank=True)
    class Meta:
        model = Experience
        fields = ['id','candidate','title','description','company','location','tech_tags','duration']

class ExperienceSerializerupdater(serializers.ModelSerializer):
    candidate = ProfileSerializer
    location = SerializableCountryField(allow_blank=True)
    class Meta:
        model = Experience
        fields = ['id','candidate','title','description','company','location','tech_tags','duration']


class ProjectSerializer(serializers.ModelSerializer):
    candidate = ProfileSerializer()
    project = MainProjectSerializer()
    class Meta:
        model = Portfolio
        fields = ['id','candidate','title','description','repository_link','demo_link','tech_tags','csa','project','likes','dislikes']

class ProjectSerializerupdater(serializers.ModelSerializer):
    candidate = ProfileSerializer
    class Meta:
        model = Portfolio
        fields = ['id','candidate','title','description','repository_link','demo_link','tech_tags','csa','project','likes','dislikes']


class ProjectAsign(serializers.ModelSerializer):
    class Meta:
        model = candidatesprojects
        fields = '__all__'

class TestCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCenter
        fields = ('id','venue','country', 'start_time', 'end_time', 'location')

class AssesmentSerializer(serializers.ModelSerializer):
    candidate = ProfileSerializer()
    project = MainProjectSerializer()
    test_center = TestCenterSerializer()
    portfolio = ProjectSerializer()
    class Meta:
        model = Assessment
        fields = ('id','candidate','project', 'stage','projectstarttime','frameworktested','test_center','test_choice','csa','portfolio')
class AssesmentSerializermini(serializers.ModelSerializer):
    candidate = ProfileSerializer
    project = MainProjectSerializer()
    test_center = TestCenterSerializer()
    class Meta:
        model = Assessment
        fields = ('id','candidate','project', 'stage','projectstarttime','frameworktested','test_center','test_choice','csa','portfolio')

class AssesmentSerializerUpdater(serializers.ModelSerializer):
    candidate = ProfileSerializer
    project = MainProjectSerializer
    class Meta:
        model = Assessment
        fields = ('id','candidate','project', 'stage','projectstarttime','frameworktested','test_center','test_choice','csa','portfolio')

class AssesmentReportSerializer(serializers.ModelSerializer):
    candidate = ProfileSerializer()
    project = MainProjectSerializer()
    class Meta:
        model = AssessmentReport
        fields = ('id','candidate','project', 'score',)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = '__all__'

from classroom.serializers import SubjectSerializer

class ResourceSerializerupdater(serializers.ModelSerializer):

    class Meta:
        model = Resources
        fields = ('id','title','link', 'subject','created','provider','likes','tags','dislikes')
class ResourceSerializercreater(serializers.ModelSerializer):

    class Meta:
        model = Resources
        fields = ('id','title','link', 'subject','created','provider','tags')
class ResourceSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Resources
        fields = ('id','title','link', 'subject','created','provider','likes','tags','verified','dislikes')