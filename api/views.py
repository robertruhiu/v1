from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import EnterpriseAPIKey, EnterpriseProject, EnterpriseDeveloper
from api.serializers import EnterpriseDeveloperReport, \
    EnterpriseProjectSerializer, EnterpriseDeveloperReportSerializer


# Create your views here.

class EnterpriseProjects(generics.ListAPIView):
    # permission_classes = [HasAPIKey]
    serializer_class = EnterpriseProjectSerializer

    queryset = EnterpriseProject.objects.all()

    def list(self, request):
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise.projects
        # queryset = self.get_queryset()
        serializer = EnterpriseProjectSerializer(enterprise, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny,])
def schedule_test(request):
    if request.method == 'POST':
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise

        username = request.data.get('username')
        email = request.data.get('email')
        project_id = request.data.get('project_id')
        select_time = request.data.get('select_time')
        project = EnterpriseProject.objects.get(pk=project_id)
        dev = EnterpriseDeveloper.objects.get_or_create(username=username, email=email, project=project,
                                                        select_time=select_time)
        dev
        return Response('You have successfully scheduled a test. '
                        'At the appointed time a link will be sent '
                        'to you with the workspace you should use. ')


# class ScheduleTest(APIView):
#     # queryset = EnterpriseProject.objects.all()
#
#     pass

#
# class EnterpriseReport(generics.RetrieveAPIView):
#     # permission_classes = [HasAPIKey]
#     serializer_class = EnterpriseDeveloperReport
#
#     def get(self, request):
#         key = request.headers.get('Api-Key')
#         key_prefix, _, _ = key.split('.')
#         enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
#         enterprise = enterprise_api_key.enterprise.projects
#
#         # queryset = self.get_queryset()
#         serializer = EnterpriseDeveloperReport(report)
#         return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny,])
def developer_report(request):
    if request.method == 'POST':
        key = request.headers.get('Api-Key')
        key_prefix, _, _ = key.split('.')
        enterprise_api_key = EnterpriseAPIKey.objects.get_usable_keys().get(prefix=key_prefix)
        enterprise = enterprise_api_key.enterprise

        email = request.data.get('email')
        dev_report = EnterpriseDeveloperReport.objects.get(developer__email=email)
        serializer = EnterpriseDeveloperReportSerializer(dev_report)
        return Response(serializer.data)


class AllReports(generics.ListAPIView):
    # permission_classes = [HasAPIKey]
    serializer_class = EnterpriseDeveloperReport
