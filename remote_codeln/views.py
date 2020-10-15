from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView,
from rest_framework import generics

# Create your views here.
from accounts.models import Profile
from remote_codeln.models import RemoteProject, Bid, Contract, EscrowPayment
from remote_codeln.serializers import RemoteProjectSerializer, BidSerializer ,EscrowPaymentSerializer


class CreateProjectView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()


class ProjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()


class CreateBidView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.all()


class BidsListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = RemoteProject.objects.get(id=project_id)
        return Bid.objects.filter(project=project)


class CreateContractView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    pass


class ContractsListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        user_id = self.kwargs['user']
        user = Profile.objects.get(id=user_id)
        return Contract.objects.filter(user=user)


class CreateIssueView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.all()


class IssuesListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    pass


class CreatePaymentView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    pass


class PaymentListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    pass
