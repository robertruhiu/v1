from celery import task
from celery import shared_task
# We can have either registered task


@shared_task
def send_notification():
     print('Here i am')



