from rest_framework import serializers

from api.models import Enterprise, EnterpriseAPIKey, EnterpriseProject, EnterpriseDeveloper, EnterpriseDeveloperReport
from frontend.serializers import ProfileSerializer
from projects.models import Project
from projects.serializers import FrameworkSerializer


class EnterpriseIntermediateProjectSerializer(serializers.ModelSerializer):
    framework = FrameworkSerializer()
    class Meta:
        model = Project
        fields = ('id', 'name', 'brief', 'description', 'level', 'concept', 'tags',
                  'projectimage1', 'projectimage2', 'projectimage3', 'projectimage4', 'projectimage5',
                  'requirement1', 'requirement2', 'requirement3', 'requirement4', 'requirement5',
                  'duration', 'framework',)


class EnterpriseSerializer(serializers.ModelSerializer):
    user = ProfileSerializer

    class Meta:
        model = Enterprise
        fields = ('user', 'company_name', 'country',)


class EnterpriseAPIKeySerializer(serializers.ModelSerializer):
    enterprise = EnterpriseSerializer

    class Meta:
        model = EnterpriseAPIKey
        fields = ('enterprise',)


class EnterpriseProjectSerializer(serializers.ModelSerializer):
    # enterprise = EnterpriseSerializer
    project = EnterpriseIntermediateProjectSerializer()

    class Meta:
        model = EnterpriseProject
        fields = ('slug', 'project',)


class EnterpriseDeveloperSerializer(serializers.ModelSerializer):
    project = EnterpriseProjectSerializer()

    class Meta:
        model = EnterpriseDeveloper
        fields = ('username', 'email', 'project', 'select_time', 'project_completed', 'metadata')


class EnterpriseDeveloperReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnterpriseDeveloperReport
        fields = ('requirements', 'competency', 'grading', 'score', 'skill', 'code_base', 'project_description')
