from django.shortcuts import render
from rest_framework.permissions import  IsAuthenticated

from rest_framework import generics

# Create your views here.
from accounts.models import Profile
from remote_codeln.models import RemoteProject, Bid, Issue, EscrowPayment
from remote_codeln.serializers import RemoteProjectSerializer, BidSerializer ,EscrowPaymentSerializer, IssueSerializer


class CreateProjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()


class ProjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()


class CreateBidView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.all()


class BidsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = RemoteProject.objects.get(id=project_id)
        return Bid.objects.filter(project=project)


class CreateContractView(generics.CreateAPIView):
    pass


class ContractsListView(generics.ListAPIView):
    pass


class CreateIssueView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()


class IssuesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user_id = self.kwargs['user']
        user = Profile.objects.get(id=user_id)
        return Issue.objects.filter(user=user)


class CreatePaymentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    pass


class PaymentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pass
