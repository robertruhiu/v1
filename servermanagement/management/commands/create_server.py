import datetime

import pytz
from decouple import config
from django.core.management.base import BaseCommand
from django.http.response import HttpResponse

DO_TOKEN = config('DO_TOKEN', default='DO_TOKEN')

do_headers = {'Content-Type': 'application/json',
              'Authentication': f"Bearer {DO_TOKEN}"}

# from jobs.views import test_create_server

from decouple import config

DO_TOKEN = config('DO_TOKEN', default='DO_TOKEN')
DO_DOMAIN = config('DO_DOMAIN', default='DO_DOMAIN')
from servermanagement.models import Job, Server, CandidateSetup, ServerConfig



def test_create_server(request=None):
    jobs = Job.objects.filter(has_executed=False,
                              type='create_server',
                              time__date=datetime.datetime.now(tz=pytz.UTC).date())

    for job in jobs:
        if datetime.datetime.now().hour - job.time.hour < 3:
            project_name = job.data['project_name']
            setup_code = job.data['setup_code']
            candidate_id = job.data['candidate_id']
            server_type = 'ide_server_config'

            setup, created = CandidateSetup.objects.get_or_create(project_name=project_name, setup_code=setup_code,
                                                                  candidate_id=candidate_id, start_time=job.time,
                                                                  project=job.project)
            if created:
                print('reached server created Ist run')
                server_config = ServerConfig.objects.get(type=server_type)
                created_server_id, domain_name = server_config.create_server()
                Server.objects.create(machine_id=created_server_id, setup_code=setup_code,
                                      url=f'{domain_name}.{DO_DOMAIN}')
            else:
                print('reached server created 2nd run')
                server = Server.objects.get(setup_code=setup_code)
                if server.get_create_status():
                    server.assign_domain(server.url.split('.')[0])
                    job.has_executed = True
                    job.save()
                    Job.objects.create(type='create_workspace', project=job.project,
                                       data={'setup_code': job.data['setup_code'],
                                             'candidate_id': job.data['candidate_id']})
    return HttpResponse('Ok')


class Command(BaseCommand):
    help = 'Checks for jobs of type create_server and have today\'s date'

    def handle(self, *args, **kwargs):
        print('reached')
        test_create_server()
