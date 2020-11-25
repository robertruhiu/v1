import json
import datetime


import requests
from decouple import config
from django.utils.html import urlize
from django.db import models
from datetime import timedelta
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User

# Create your models here.
from accounts.models import Profile

import uuid

class RemoteProject(models.Model):
    PROJECT_TYPE = (
        ('website', 'Website'),
        ('android-App', 'Android App'),
        ('ios-App', 'Ios App'),
        ('Desktop-App', 'Desktop Application'),
    )

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, max_length=200)
    tools = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client', blank=True, null=True)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project_type = models.CharField(max_length=40, choices=PROJECT_TYPE, default='website')
    team_size = models.CharField(max_length=20, choices=(
        ('single_dev', 'Single Developer'),
        ('team', 'Multiple Developers')), default='single_dev')
    budget = models.IntegerField(default=15)
    timeline = models.DurationField(default=timedelta(days=14))
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            name = f'{self.title}-{uuid.uuid4()}'
            self.slug = slugify(name)
        super().save(*args, **kwargs)


class RemoteDeveloper(models.Model):
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)


class ProjectFeature(models.Model):
    name = models.CharField(max_length=120)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, max_length=200)
    amount = models.IntegerField(default=15)
    due_date = models.DateTimeField()
    assigned_to = models.ForeignKey(RemoteDeveloper, on_delete=models.CASCADE, blank=True, null=True)
    escrow_disbursed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FeatureStory(models.Model):
    feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
    user_story = models.TextField(blank=True)


class Tasks(models.Model):
    STAGE = (
        ('backlog', 'Backlog'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),

    )
    feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    stage = models.CharField(max_length=40, choices=STAGE, default='backlog')
    assigned_to = models.ForeignKey(RemoteDeveloper, on_delete=models.CASCADE, blank=True, null=True)


class EscrowPayment(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=15)
    data = JSONField(default=dict)
    paid_at = models.DateTimeField(auto_now=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)


class Bid(models.Model):
    budget = models.IntegerField(default=15, null=True, blank=True)
    developer = models.ForeignKey(RemoteDeveloper, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(RemoteProject, on_delete=models.CASCADE, blank=True, null=True)
    timeline = models.DurationField(default=timedelta(days=14))
    tools = models.TextField(null=True, blank=True)
    shortlisted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)


class Issue(models.Model):
    feature = models.ForeignKey(ProjectFeature, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    arbitration_required = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    text = models.TextField(blank=True)

headers = {'Content-Type': 'application/json', 'Api-Token': config('SendBird_API_TOKEN', default='default'),
               'charset': 'utf8'}

class Chat(models.Model):
    ids = models.CharField(max_length=300, blank=True)
    users = ArrayField(models.CharField(max_length=140), size=3, blank=True, null=True, unique=True)
    channel_url = models.CharField(max_length=300, null=True, blank=True, editable=False)
    messages = JSONField(null=True, blank=True, default=dict)
    name = models.CharField(max_length=140, blank=True)
    unread_counts = JSONField(null=True, blank=True, default=dict)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    @staticmethod
    def send_message(sender, receiver, channel_url, message, has_attachment=False):
        chat = Chat.objects.get(channel_url=channel_url)
        if len(message) == 0 and has_attachment:
            message = 'Find attached ...'
        sendbird_message = {
            "message_type": "MESG",
            "user_id": sender,
            "message": message
        }
        sendbird_res = requests.post(
            'https://api-{}.sendbird.com/v3/group_channels/{}/messages'.format(
                config("SendBird_APP_ID", default="SendBird_APP_ID"),
                chat.channel_url),
            headers=headers,
            data=json.dumps(sendbird_message))
        message_id = json.loads(sendbird_res.content)['message_id']

        message_obj = {
            'message': urlize(message, nofollow=True).replace('rel="nofollow"',
                                                              'target="_blank" rel="noopener noreferrer"'),
            'messageId': message_id,
            'messageType': 'MESG',
            '_sender': {
                'userId': sender,
                'nickname': str(User.objects.get(username=sender).profile)
            },
            'created': str(datetime.datetime.now())
        }
        if chat.messages == "[]":
            chat.messages = json.dumps([message_obj])
            chat.save()
        else:
            new_chat_messages = json.loads(chat.messages)
            new_chat_messages.append(message_obj)
            chat.messages = json.dumps(new_chat_messages)
            chat.save()
        return {'message_id': message_id, 'messages': chat.messages}



    def __str__(self):
        return self.name

    @property
    def get_messages(self):
        return json.loads(self.messages)

    @property
    def all_users(self):
        return [User.objects.get(username=username) for username in self.users]
