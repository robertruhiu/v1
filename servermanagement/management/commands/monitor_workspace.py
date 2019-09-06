import json
import datetime

from django.core.management.base import BaseCommand

from jobs.models import Job, CandidateSetup



class Command(BaseCommand):
    help = 'Monitor workspace watch time and monitor workspace'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(has_executed=False, type='monitor_workspace')
        for job in jobs:
            candidate = CandidateSetup.objects.get(setup_code=job.data['setup_code'])
            if datetime.datetime.now(datetime.timezone.utc) > candidate.start_time + job.project.transaction.project.duration:
                candidate.project_completed = True
                candidate.save()
                # TODO: get this from job model no need for query
                project = Job.objects.get(type='create_server', data__setup_code=job.data['setup_code']).project
                project.stage = 'project_completed'
                project.save()
                job.has_executed = True
                job.save()
                Job.objects.create(type='start_analysis', project=job.project, data={'setup_code': job.data['setup_code'], 'candidate_id': job.data['candidate_id']})