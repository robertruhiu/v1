from __future__ import absolute_import
import os
from celery import Celery
from decouple import config
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codelnmain.settings')
app = Celery('codelnmain',
             broker=config('REDIS_URL', default='redis://'),
             backend=config('REDIS_BACKEND', default='redis://'),)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)