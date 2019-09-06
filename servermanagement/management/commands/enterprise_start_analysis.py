import requests

from django.core.management.base import BaseCommand

from jobs.models import EnterpriseJob, Server, EnterpriseCandidateSetup



class Command(BaseCommand):
    help = 'Trigger Candidate server to start file preparation'

    def handle(self, *args, **options):
        jobs = EnterpriseJob.objects.filter(has_executed=False, type='start_analysis')
        for job in jobs:
            setup_code = job.data['setup_code']
            candidate = EnterpriseCandidateSetup.objects.get(setup_code=job.data['setup_code'])
            container_name = candidate.workspace_data['id']
            server = Server.objects.get(setup_code=setup_code)
            url = server.url
            res = requests.get(f'http://{url}/prepare-files/', params={'container_name': container_name})
            project = EnterpriseJob.objects.get(type='create_server', data__setup_code=job.data['setup_code']).project
            project.stage = 'analysis_started'
            project.save()
            job.has_executed = True
            job.save()
            EnterpriseJob.objects.create(type='transfer_files',  project=job.project,
                                             data={'setup_code': job.data['setup_code'],
                                                   'candidate': job.data['candidate']})