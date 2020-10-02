from django.shortcuts import render
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView


# Create your views here.


class CreateProjectView(APIView):
    permission_classes = [AllowAny,]
    pass


class ProjectListView(APIView):
    permission_classes = [AllowAny,]
    pass


class CreateBidView(APIView):
    permission_classes = [AllowAny,]
    pass


class BidsListView(APIView):
    permission_classes = [AllowAny,]
    pass


class CreateContractView(APIView):
    permission_classes = [AllowAny,]
    pass


class ContractsListView(APIView):
    permission_classes = [AllowAny,]
    pass


class CreateIssueView(APIView):
    permission_classes = [AllowAny,]
    pass


class IssuesListView(APIView):
    permission_classes = [AllowAny,]
    pass
