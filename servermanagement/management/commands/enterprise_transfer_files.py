import json
import requests

from django.core.management.base import BaseCommand

from jobs.models import EnterpriseJob, Server, EnterpriseCandidateSetup



class Command(BaseCommand):
    help = 'Trigger Candidate server to transfer files to jenkins'

    def handle(self, *args, **options):
        jobs = EnterpriseJob.objects.filter(has_executed=False, type='transfer_files')
        for job in jobs:
            setup_code = job.data['setup_code']
            candidate = EnterpriseCandidateSetup.objects.get(setup_code=job.data['setup_code'])
            container_name = candidate.workspace_data['id']
            server = Server.objects.get(setup_code=setup_code)
            url = server.url
            company = job.project.enterprise_project.user.profile.company
            candidate_name = f'{job.project.enterprise_candidatecandidate.first_name}-{job.project.candidate.last_name}'
            project_name = job.project.enterprise_project.project.name
            framework = job.project.enterprise_project.project.framework.name.lower()
            res = requests.get(f'http://{url}/send-files/',
                               params={'container_name':container_name, 'candidate_name':candidate_name,
                                       'company':company, 'project_name': project_name, 'framework':framework})
            project = EnterpriseJob.objects.get(type='create_server', data__setup_code=job.data['setup_code']).project
            project.stage = 'transfer_complete'
            project.save()
            job.has_executed = True
            job.save()
            # shut down server
            # TODO: create job to shut down server
            EnterpriseJob.objects.create(type='get_analysis', project=job.project,data={'setup_code': job.data['setup_code'],'candidate_id': job.data['candidate_id']})