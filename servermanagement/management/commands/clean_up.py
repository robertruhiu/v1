import json

import requests
from decouple import config
from django.core.management.base import BaseCommand

from jobs.models import Job, CandidateSetup, Server


class Command(BaseCommand):
    help = 'Shuts down server, Deletes Droplet, unassigns domain name'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(has_executed=False, type='clean_up')
        for job in jobs:
            setup_code = job.data['setup_code']
            candidate = CandidateSetup.objects.get(setup_code=job.data['setup_code'])

            if "component" in candidate.report:
                server = Server.objects.get(setup_code=setup_code)
                server.unassign_domain(server.url.split('.')[0])
                server.shutdown_droplet()
                server.delete_droplet()
                job.has_executed = True
                job.save()
            # end of commands