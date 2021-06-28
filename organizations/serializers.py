from django.contrib.auth.models import User
from frontend.serializers import UserSerializer
from rest_framework import serializers

from organizations.models import Organization,OrganizationUser,OrganizationOwner,OrganizationInvitation


class AllOrganizationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationsOwnersSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrganizationOwner
        fields = '__all__'
class OrganizationsUsersSerializersCreate(serializers.ModelSerializer):

    class Meta:
        model = OrganizationUser
        fields = ['id','is_admin','organization','user']

class OrganizationsUsersSerializers(serializers.ModelSerializer):
    organization = AllOrganizationsSerializers()
    user = UserSerializer()
    class Meta:
        model = OrganizationUser
        fields = ['id','organization','user','is_admin']

class OrganizationsInvitationsFullSerializers(serializers.ModelSerializer):
    organization = AllOrganizationsSerializers()
    invited_by =UserSerializer()
    class Meta:
        model = OrganizationInvitation
        fields = ['id','organization','invited_by','created','invitee_id','invitee_identifier']
class OrganizationsInvitationsSerializers(serializers.ModelSerializer):
    organization = AllOrganizationsSerializers()
    class Meta:
        model = OrganizationInvitation
        fields = ['id','organization','invited_by','created','invitee_id','invitee_identifier']
class OrganizationsInvitationsCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrganizationInvitation
        fields = ['id','organization','invited_by','created','invitee_id','invitee_identifier']
