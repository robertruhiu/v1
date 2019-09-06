# from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from jobs.models import Job


class Command(BaseCommand):
    help = 'Create Digital Ocean Server'

    def handle(self, *args, **options):
        jobs = Job.objects.filter(executed=False)
        for job in jobs:
            if job.type == 'create_server':
                job.executed = True
                job.save()
