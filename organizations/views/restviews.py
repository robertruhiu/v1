from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.permissions import IsAuthenticated
from organizations.serializers import AllOrganizationsSerializers,OrganizationsOwnersSerializers,OrganizationsUsersSerializers,\
    OrganizationsInvitationsSerializers,OrganizationsUsersSerializersCreate,OrganizationsInvitationsFullSerializers,OrganizationsInvitationsCreateSerializers
from django.contrib.auth.models import User
from rest_framework import generics
from organizations.models import Organization,OrganizationUser,OrganizationOwner,OrganizationInvitation

class OrganizationList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationsUsersSerializers
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return OrganizationUser.objects.filter(user_id=user_id)


class AddOrganization(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Organization.objects.all()
    serializer_class = AllOrganizationsSerializers

class AddOrganizationOwner(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationOwner.objects.all()
    serializer_class = OrganizationsOwnersSerializers

class FetchOrganization(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Organization.objects.all()
    serializer_class = AllOrganizationsSerializers

class EditOrganization(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Organization.objects.all()
    serializer_class = AllOrganizationsSerializers

class DeleteOrganization(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Organization.objects.all()
    serializer_class = AllOrganizationsSerializers

class OrganizationUserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationsUsersSerializers
    def get_queryset(self):
        organization_pk = self.kwargs['organization_pk']
        return OrganizationUser.objects.filter(organization=organization_pk)

class OrganizationUserAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationsUsersSerializersCreate

class OrganizationUserUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationsUsersSerializers

class OrganizationUserDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationsUsersSerializers

class OrganizationUserCreateInvitation(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationInvitation.objects.all()
    serializer_class = OrganizationsInvitationsCreateSerializers

class InviteEmail(generics.RetrieveAPIView):
    serializer_class = OrganizationsInvitationsFullSerializers

    def get_queryset(self):
        email = self.kwargs['email']
        organization_id = self.kwargs['organization_pk']
        organization = OrganizationUser.objects.get(id=organization_id)

        subject = 'You have been invited to join a team'
        html_message = render_to_string('organizations/inviteemail.html',
                                        {'organization': organization})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


        return OrganizationInvitation.objects.all()

class UserGetInvitations(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationsInvitationsFullSerializers
    def get_queryset(self):
        user_email = self.kwargs['email']
        return OrganizationInvitation.objects.filter(invitee_identifier=user_email)

class OrganizationGetInvitations(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationsInvitationsSerializers
    def get_queryset(self):
        organization_id = self.kwargs['organization_pk']
        organization = Organization.objects.get(id=organization_id)
        return OrganizationInvitation.objects.filter(organization=organization)

class OrganizationUserSendInvitation(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationInvitation.objects.all()
    serializer_class = OrganizationsInvitationsSerializers

class RemoveUser(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationsUsersSerializers

class DeleteInvite(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationInvitation.objects.all()
    serializer_class = OrganizationsInvitationsSerializers