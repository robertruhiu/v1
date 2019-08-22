from rest_framework import serializers

from projects.models import Project, Framework, Devtype, Projecttype, Language
from  frontend.models import AssessmentReport


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name',)


class FrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = '__all__'


class DevtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devtype
        fields = ('name',)


class ProjecttypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projecttype
        fields = ('name',)


class Projectserializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
