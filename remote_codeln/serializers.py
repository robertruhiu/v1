from rest_framework import serializers

from remote_codeln.models import RemoteProject, Bid, EscrowPayment, Issue, ProjectFeature, FeatureStory, Tasks, \
    Comments, RemoteDeveloper, Team, Files, Signatures, Chat
from frontend.serializers import ProfileSerializer


class RemoteProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteProject
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    project = RemoteProjectSerializer()

    class Meta:
        model = Bid
        fields = ['id', 'developer', 'accepted', 'proposal', 'shortlisted', 'tools',
                  'project', 'budget', 'timeline']


class BidSerializerBasic(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'


class RemoteDeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteDeveloper
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = ProfileSerializer()

    class Meta:
        model = Tasks
        fields = ['id', 'feature', 'stage', 'description', 'assigned_to']


class TaskSerializerUpdater(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


class EscrowPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowPayment
        fields = ['client', 'project', 'amount', 'data']


class FeatureSerializerDetail(serializers.ModelSerializer):
    project = RemoteProjectSerializer()

    class Meta:
        model = ProjectFeature
        fields = ['id', 'name', 'project']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class IssueSerializerDetail(serializers.ModelSerializer):
    feature = FeatureSerializerDetail()

    class Meta:
        model = Issue
        fields = ['id', 'feature', 'title', 'description', 'arbitration_required', 'closed', 'tag']


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Comments
        fields = ['id', 'issue', 'text', 'author', 'created']


class CommentSerializerBasic(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFeature
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureStory
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


# File manager serializer
class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


class SignaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signatures
        fields = '__all__'


class JSONSerializerField(serializers.Field):
    """ Serializer for JSONField -- required to make field writable"""

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    messages = serializers.JSONField()

    class Meta:
        model = Chat
        fields = ['id', 'ids', 'users', 'channel_url', 'messages','name']
