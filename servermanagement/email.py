from decouple import config
from django.core.mail import  send_mail, EmailMultiAlternatives
from django.http import HttpResponse



def setup_finished_mail(recipient, url):
    subject = 'Hi there your test is ready!'
    message = f'Your Workspace is ready.\n Go to {url} to start project'
    email_from =  config('EMAIL_HOST_USER')
    request = [recipient]

    send_mail(subject, message, email_from, request)
    return  HttpResponse('OK')

def approve_candidate_mail(candidate, country, date_time, email, automate_url, manual_url):
    subject = f'{candidate} has requested a test on {date_time}'
    message = f'Candidate Location : {country}. ' \
              f'Email Address : {email}' \
              f'Approve Candidate for Automated Test : {automate_url}  or' \
              f'Select Candidate for Manual Test : {manual_url}'
    email_from = config('EMAIL_HOST_USER')
    request = ['philisiah@codeln.com']

    send_mail(subject, message, email_from, request)
    return HttpResponse('OK')

def automated_notification_mail(recipient, time):
    subject = 'Hi there'
    message = f'You have successfully scheduled your test at {time}! ' \
              f'at the appointed time you will recieve the link to your workspace.' \
              f'Happy Coding!'
    email_from =  config('EMAIL_HOST_USER')
    request = [recipient]

    send_mail(subject, message, email_from, request)
    return  HttpResponse('OK')

def automated_test_chosen(recipient, candidate, time, project, framework):
    subject = f'{candidate} Automated Test'
    message = f'{candidate} has been selected for automated test at {time}! ' \
              f'for {project} in {framework}' \
              f'Happy Coding!'
    email_from =  config('EMAIL_HOST_USER')
    request = [recipient]

    send_mail(subject, message, email_from, request)
    return  HttpResponse('OK')

def manual_notification_mail(recipient, time):
    subject = 'Hi there'
    message = f'You have successfully scheduled your test at {time}! ' \
              f'Our Test engineer will contact you with details on your test.' \
              f'Happy Coding!'
    email_from =  config('EMAIL_HOST_USER')
    request = [recipient]
    send_mail(subject, message, email_from, request)
    return  HttpResponse('OK')

def enterprise_notification_mail( firstname, lastname, recipient,token, url='https://app.goodtalent.dev'):
    subject = f'Good day {firstname} {lastname}'
    message = f'You have been invited to take a test on Good talent. Follow this URL {url} to schedule a time for your test.' \
              f'Your login Informatio is as follows: ' \
              f'email:{recipient}' \
              f'authentication: {token}' \
              f'At the appointed time you will recieve the link to your workspace.Happy Coding!'
    email_from =  config('EMAIL_HOST_USER')
    request = [recipient]
    send_mail(subject, message, email_from, request)
    return  HttpResponse('OK')