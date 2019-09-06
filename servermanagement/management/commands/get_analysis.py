import requests
from decouple import config
from django.core.management.base import BaseCommand

from jobs.models import Job, CandidateSetup


class Command(BaseCommand):
    help = 'Get Sonarqube analysis'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(has_executed=False, type='get_analysis')
        for job in jobs:
            setup_code = job.data['setup_code']
            candidate = CandidateSetup.objects.get(setup_code=job.data['setup_code'])
            jenkins_url = config('JENKINS_URL', default='JENKINS_URL')
            company = job.project.transaction.user.profile.company
            candidate_name = f'{job.project.candidate.first_name}-{job.project.candidate.last_name}'
            projectKey = "{}-{}".format(company.lower(), candidate_name.lower())
            sonarqube_api = f'https://{jenkins_url}/sonar/api/measures/component?componentKey={projectKey}&&metricKeys=' \
            'classes,comment_lines,directories,files,ncloc,functions,violations,code_smells,sqale_rating,coverage,' \
            'complexity,cognitive_complexity,duplicated_blocks,duplicated_lines,duplicated_files,' \
            'duplicated_lines_density,sqale_index,vulnerabilities,alert_status,quality_gate_details,bugs,' \
            'security_rating,tests,test_failures,test_errors,class_complexity'
            res = requests.post(sonarqube_api).json()
            candidate.report = res
            candidate.save()
            project = Job.objects.get(type='create_server', data__setup_code=job.data['setup_code']).project
            project.stage = 'analysis_complete'
            project.save()
            job.has_executed = True
            job.save()
            # TODO: create job to clean up and destroy server check if response has data
            Job.objects.create(type='clean_up', project=job.project,data={'setup_code': job.data['setup_code'],'candidate_id': job.data['candidate_id']})