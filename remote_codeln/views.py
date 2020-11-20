import hmac
import json
import uuid

import requests
from decouple import config
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics

# Create your views here.
from accounts.models import User, Profile
from remote_codeln.models import RemoteProject, Bid, Issue, EscrowPayment, Chat
from remote_codeln.serializers import RemoteProjectSerializer, BidSerializer, EscrowPaymentSerializer, IssueSerializer


class CreateProjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()


class ProjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()


class CreateBidView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.all()


class BidUpdateView(generics.RetrieveUpdateDestroyAPIView):
    pass


class BidsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = RemoteProject.objects.get(id=project_id)
        return Bid.objects.filter(project=project)


class CreateContractView(generics.CreateAPIView):
    pass


class ContractsListView(generics.ListAPIView):
    pass


class CreateIssueView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()


class IssuesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user_id = self.kwargs['user']
        user = Profile.objects.get(id=user_id)
        return Issue.objects.filter(user=user)


class CreatePaymentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    pass


class PaymentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pass

class SendMessageView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pass

sendbird_headers = {'Content-Type': 'application/json', 'Api-Token': config('SendBird_API_TOKEN', default='default'),
                    'charset': 'utf8'}
def chats(request):
    conversations = []
    for chat in Chat.objects.filter(users__overlap=[request.user.username]).order_by('-updated'):
        try:
            if len(chat.messages) > 10:  # "[]" is less than 10
                other_user = ''
                messages = json.loads(chat.messages)
                try:
                    last_message = messages[len(messages) - 1]['message']
                    last_message = (last_message[:140] + '...') if len(last_message) > 140 else last_message
                except (KeyError, IndexError) as e:
                    last_message = '...'

                for username in chat.users:
                    if username != request.user.username:
                        other_user = User.objects.get(username=username)
                conversations.append(
                    {'avatar': other_user.profile.thumbnail, 'name': str(other_user.profile),
                     'username': other_user.username,
                     'lastMessage': last_message})
        except:
            pass
    context = {
        'chats': True,
        'conversations': json.dumps(conversations)
    }
    return JsonResponse(request, data=context)



def chat_with(request):
    user = request.GET.get('user')
    other_user = request.GET.get('other_user')
    if user == other_user:
        # someone tried chatting with self
        return JsonResponse('chatting with self')
    cur_user = User.objects.get(username=user)
    other_user = User.objects.get(username=other_user)
    chat, created = Chat.objects.get_or_create(
        users=sorted([user.username, other_user.username]),
        ids=','.join(sorted([user.username, other_user.username])))

    def __create_channel(chat):
        chat.name = "Chat between {} and {}".format(cur_user.get_full_name(),
                                                    other_user.get_full_name())
        for user in [cur_user, other_user]:
            requests.post(f'https://api-{config("SendBird_APP_ID", default="SendBird_APP_ID")}.sendbird.com/v3/users',
                          headers=sendbird_headers,
                          data=json.dumps({
                              "user_id": user.username,
                              "nickname": str(user.profile),
                              "profile_url": str(user.profile.get_absolute_url())
                          }))
        get_or_create_channel_res = requests.post(
            f'https://api-{config("SendBird_APP_ID", default="SendBird_APP_ID")}.sendbird.com/v3/group_channels',
            headers=sendbird_headers,
            data=json.dumps({
                "name": chat.name,
                "user_ids": chat.users,
                "is_distinct": True
            }))
        if get_or_create_channel_res.status_code == 500:
            # capture_message("SendBird failed to create channel", level="critical")
            # messages.error(request, "An unexpected error occurred. Please try again")
            return JsonResponse(request.META['HTTP_REFERER'])
        chat.channel_url = json.loads(get_or_create_channel_res.content)['channel_url']
        chat.save()

    if created:
        __create_channel(chat)
    else:
        res = requests.get(
            f'https://api-{config("SendBird_APP_ID", default="SendBird_APP_ID")}.sendbird.com/v3/group_channels/{chat.channel_url}',
            headers=sendbird_headers)
        if res.status_code == 200:
            pass
        else:
            __create_channel(chat)
    # try:
    #     async_mark_messages_read(user.username, chat.channel_url)
    # except Exception as e:
    #     capture_exception(e)
    if len(json.dumps(chat.messages)) < 5:
        chat.messages = json.dumps([])
        chat.save()
    context = {
        'other_user': other_user,
        'chat': chat,
        'chat_with': True,
        'UNIQUE_HANDLER_ID': str(uuid.uuid4()),
        # 'attachments_form': AttachmentForm()
    }
    return JsonResponse(request, data='context')

def send_message(request, user, other_user, channel_url):
    if request.method == 'POST':
        cur_user = User.objects.get(username=user)
        res = Chat.send_message(sender=cur_user.username,
                                receiver=other_user,
                                channel_url=channel_url, message=request.POST['message'])
        return JsonResponse(
            {'messageId': int(res['message_id']), 'tempId': request.POST['tempId'], 'messages': res['messages']})

