from rest_framework import serializers

from api.models import Enterprise, EnterpriseAPIKey, EnterpriseProject, EnterpriseDeveloper, EnterpriseDeveloperReport
from frontend.serializers import ProfileSerializer
from projects.serializers import Projectserializer


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
    project = Projectserializer()

    class Meta:
        model = EnterpriseProject
        fields = ('project',)


class EnterpriseDeveloperSerializer(serializers.ModelSerializer):
    project = EnterpriseProjectSerializer

    class Meta:
        model = EnterpriseDeveloper
        fields = ('username', 'email', 'project', 'select_time',)


class EnterpriseDeveloperReportSerializer(serializers.ModelSerializer):
    developer = EnterpriseDeveloperSerializer

    class Meta:
        model = EnterpriseDeveloperReport
        fields = ('requirements', 'competency', 'grading', 'score', 'skill', 'developer',)
