from rest_framework import serializers
from frontend.serializers import AssesmentSerializer
from servermanagement.models import Job as AssessmentJob
# from transactions.serializers import EnterpriseCandidateProjectsSerializer

class AssesmentJobSerializer(serializers.ModelSerializer):
    # candidate = ProfileSerializer()
    project = AssesmentSerializer()
    class Meta:
        model = AssessmentJob
        fields = ('id','project', 'has_executed','time','type', 'data', 'created')

# class EnterpriseCandidateSetupSerializer(serializers.ModelSerializer):
#     # project = EnterpriseCandidateProjectsSerializer()
#
#     class Meta:
#         # model = EnterpriseCandidateSetup
#         fields = ('project', 'project_name', 'setup_code',
#                   'workspace_data', 'workspace_url', 'report', 'candidate_notified',
#                   'project_completed', 'start_time', 'end_time',)


