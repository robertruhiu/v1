from django.core.management.base import BaseCommand

from jobs.email import setup_finished_mail
from jobs.models import Job, CandidateSetup


class Command(BaseCommand):
    help = 'Send email notification to candidate'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(has_executed=False, type='send_mail')
        for job in jobs:
            candidate = CandidateSetup.objects.get(setup_code=job.data['setup_code'])
            # todo: uncomment during demo
            setup_finished_mail(job.project.candidate.email, candidate.workspace_url)
            candidate.candidate_notified = True
            candidate.save()
            project = Job.objects.get(type='create_server', data__setup_code=job.data['setup_code']).project
            project.stage = 'in_progress'
            project.save()
            job.has_executed = True
            job.save()
            Job.objects.create(type='monitor_workspace', project=job.project,data={'setup_code': job.data['setup_code'], 'candidate_id': job.data['candidate_id']})