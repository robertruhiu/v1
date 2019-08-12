from rest_framework import serializers

from projects.models import Project, Framework, Devtype, Projecttype, Language
from  frontend.models import AssessmentReport


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name',)


class FrameworkSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = Framework
        fields = ('ide_stack', 'name', 'language')


class DevtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devtype
        fields = ('name',)


class ProjecttypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projecttype
        fields = ('name',)


class Projectserializer(serializers.ModelSerializer):
    framework = FrameworkSerializer()
    devtype = DevtypeSerializer()
    projecttype = ProjecttypeSerializer()

    class Meta:
        model = Project
        fields = ('id','name', 'brief', 'description', 'level', 'concept', 'tags','projectimage1', 'projectimage2', 'projectimage3',
                  'projectimage4', 'projectimage5', 'projectimage6', 'requirement1', 'requirement2',
                  'requirement3', 'requirement4', 'requirement5', 'requirement6', 'requirement7', 'framework',
                  'devtype', 'projecttype', 'project_template', 'duration')
