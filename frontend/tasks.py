# from celery import task
from codelnmain.celery import app
# We can have either registered task


# @shared_task
# def send_notification():
#      print('Here i am')
from decouple import config
from django.core.mail import send_mail


@app.task
def send_notification():
    send_mail('celery test', 'testing', 'sphilisiah@gmail.com', ['philisiah@codeln.com'])
    print('done')

