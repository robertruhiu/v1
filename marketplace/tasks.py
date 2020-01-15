# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from marketplace.models import Job
from accounts.models import Profile


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
        url = 'http://codeln.com/jobdetails/'+ job_id
        to.append(one)
        subject = 'This job fits one of your skillsets.Apply now'
        html_message = render_to_string('invitations/email/jobemails.html',{'job': job,'url':url})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)

