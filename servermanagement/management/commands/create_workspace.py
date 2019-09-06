import json

import requests
from django.core.management.base import BaseCommand

from jobs.models import Job, Server, CandidateSetup, IdeFactory

che_headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}


class Command(BaseCommand):
    help = 'Creates a workspace on the IDE to set up a working enviroment for the user'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(has_executed=False, type='create_workspace')
        for job in jobs:
            setup_code = job.data['setup_code']
            server = Server.objects.get(setup_code=setup_code)
            candidate_setup = CandidateSetup.objects.get(setup_code=setup_code)
            stack = IdeFactory.objects.get(stack=candidate_setup.project.transaction.project.framework.ide_stack)
            # TODO:factory url in scratch file
            config = stack.workspace_config
            config["projects"][0]["name"] = f'{candidate_setup.project_name}'
            config["projects"][0]["source"]["location"] = candidate_setup.project.transaction.project.project_template
            config["projects"][0]["path"] = f'/{candidate_setup.project_name}'
            config["name"] = f'{job.project.candidate.first_name}-{job.project.candidate.last_name}'
            res = requests.post(url=f'http://{server.url}:8080/api/workspace?start-after-create=true',
                                data=json.dumps(
                                    config
                                ),
                                headers=che_headers).json()
            print(res)
            candidate_setup.workspace_data = res
            candidate_setup.set_end_time()
            workspace_name = f'{job.project.candidate.first_name}-{job.project.candidate.last_name}'
            time = candidate_setup.end_time.timestamp()
            url = server.url
            resp = requests.get(f'http://{url}/ide-user/',
                                params={'workspace_name': workspace_name, 'time': time, 'url': url})
            candidate_setup.workspace_url = f'http://{server.url}'
            candidate_setup.save()
            project = Job.objects.get(type='create_server', data__setup_code=setup_code).project
            project.stage = 'link_available'
            project.save()
            job.has_executed = True
            job.save()
            # job that sends candidate email/notification on platform
            Job.objects.create(type='send_mail', project=job.project,
                               data={'setup_code': job.data['setup_code'],
                                     'candidate_id': job.data['candidate_id']})
