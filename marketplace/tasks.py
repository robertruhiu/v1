# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from marketplace.models import Job
from accounts.models import Profile
from decouple import config
from cryptography.fernet import Fernet
from datetime import date,datetime,time
from marketplace.models import JobApplication
@shared_task
def send_email(job_id):
    job = Job.objects.get(id=job_id)
    skills = job.tech_stack.split(",")
    dev_profiles = Profile.objects.select_related('user').exclude(skills__isnull=True).filter(user_type='developer')

    emails = []
    for one_profile in dev_profiles:
        dev_skills = one_profile.skills.split(",")
        if (set(skills) & set(dev_skills)) and one_profile.country ==job.location:
            emails.append(one_profile.user.email)
    for one in emails:
        to =[]
        url = 'http://codeln.com/jobdetails/'+ str(job_id)
        to.append(one)
        subject = 'This job fits one of your skillsets.Apply now'
        html_message = render_to_string('invitations/email/jobemails.html',{'job': job,'url':url})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)

@shared_task
def weekly_applicants():
    current_week = datetime.date(datetime.now()).isocalendar()[1]
    current_year = datetime.date(datetime.now()).isocalendar()[0]

    key = config('KEY', default='KEY').encode()


    # # current week applications
    recruiters = []
    # applications = JobApplication.objects.filter(created__week=current_week,created__year=current_year).filter(recruiter__pk = 1)
    applications = JobApplication.objects.filter(created__week=current_week).filter(created__year=current_year).filter(recruiter__notifications=True)

    # applications = JobApplication.objects.filter(created_date__iso_year=current_year).filter(created_date__week=current_week)
    for one in applications:
        recruiters.append(one.recruiter)
    unique_recruiters = set(recruiters)
    for one in unique_recruiters:
        recruiter_applications = JobApplication.objects.filter(created__week=current_week,created__year=current_year).filter(recruiter__pk = one.id)


        all_applications = len(recruiter_applications)
        new =0
        active =0
        testing =0
        interview =0
        for one_recruiter_application in recruiter_applications:
            if one_recruiter_application.stage == 'active':
                active += 1
            elif one_recruiter_application.stage == 'test':
                testing += 1
            elif one_recruiter_application.stage == 'interview':
                interview += 1
            elif one_recruiter_application.stage == 'new':
                new += 1

        message = str(one.id).encode()
        f = Fernet(key)
        encrypted = f.encrypt(message)
        token = encrypted.decode()
        unsubscribe_url = 'http://codeln.com/unsubscribe/' + token
        to = [one.user.email]
        subject = 'Your weekly applicants update'
        html_message = render_to_string('invitations/email/recruiterweekly.html', {'all_applications': all_applications,'active':active,'testing':testing,'interview':interview,'new':new, 'unsubscribe_url': unsubscribe_url})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)







