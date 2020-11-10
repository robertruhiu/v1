from django.core import mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.permissions import  IsAuthenticated
from django.http import JsonResponse
from rest_framework import generics

# Create your views here.
from accounts.models import Profile
from remote_codeln.models import RemoteProject, Bid, Issue, EscrowPayment,FeatureStory,ProjectFeature,Tasks,Comments,\
    RemoteDeveloper,Team,Files
from remote_codeln.serializers import RemoteProjectSerializer, BidSerializer ,EscrowPaymentSerializer, \
    IssueSerializer,FeatureSerializer,StorySerializer,BidSerializerBasic,TaskSerializer,CommentSerializer\
    ,CommentSerializerBasic,RemoteDeveloperSerializer,IssueSerializerDetail,TeamSerializer,TaskSerializerUpdater,FilesSerializer
from frontend.serializers import UserSerializer
from django.contrib.auth.models import User
# project
class CreateProjectView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()

class ProjectUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RemoteProjectSerializer
    queryset = RemoteProject.objects.all()

class GetProject(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RemoteProjectSerializer
    queryset = RemoteProject.objects.all()

class GetProjectSlug(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RemoteProjectSerializer
    lookup_field = 'slug'
    queryset = RemoteProject.objects.all()

class ProjectListView(generics.ListAPIView):


    serializer_class = RemoteProjectSerializer

    def get_queryset(self):
        return RemoteProject.objects.all()

class ProjectOwnerListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RemoteProjectSerializer
    lookup_field = 'owner'
    def get_queryset(self):
        posted = Profile.objects.get(pk=self.kwargs['owner'])
        if posted.user.is_staff:
            return RemoteProject.objects.all()


        else:
            return RemoteProject.objects.filter(client__id = self.kwargs['owner'])




class ProjectDeveloperListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RemoteProjectSerializer
    lookup_field = 'assigned_to'


    def get_queryset(self):
        return RemoteProject.objects.filter( assigned_to_id=self.kwargs['assigned_to'])

# features

class CreateFeatureView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeatureSerializer

    def get_queryset(self):
        return ProjectFeature.objects.all()

class ProjectFeatureGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeatureSerializer

    def get_queryset(self):
        return ProjectFeature.objects.filter(project__pk = self.kwargs['pk'])

class FeatureGet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeatureSerializer
    queryset = ProjectFeature.objects.all()



class ProjectFeatureUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ProjectFeature.objects.all()
    serializer_class = FeatureSerializer

class ProjectFeatureDelete(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeatureSerializer
    def get_queryset(self):
        instance = ProjectFeature.objects.get(pk = self.kwargs['pk'])
        instance.delete()
        return ProjectFeature.objects.all()

class FinishedFeature(generics.RetrieveAPIView):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        feature_id = self.kwargs['pk']
        currentfeature = ProjectFeature.objects.get(id=feature_id)
        subject = 'The following feature has been completed.Please review'
        html_message = render_to_string('emails/finishedmilestone.html',{'feature': currentfeature})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = currentfeature.project.client.user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return ProjectFeature.objects.all()

# stories

class CreateStoriesView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = StorySerializer

    def get_queryset(self):
        return FeatureStory.objects.all()

class FeatureStoryGet(generics.ListAPIView):

    serializer_class = StorySerializer

    def get_queryset(self):
        return FeatureStory.objects.filter(feature__id =self.kwargs['pk'])

class FeatureStoryUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = StorySerializer
    queryset = FeatureStory.objects.all()

class FeatureStoryDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = StorySerializer
    def get_queryset(self):
        instance = FeatureStory.objects.get(pk = self.kwargs['pk'])
        instance.delete()
        return FeatureStory.objects.all()


#bids
class BidUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializerBasic
    queryset = Bid.objects.all()

class CreateBidView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializerBasic

    def get_queryset(self):

        return Bid.objects.all()

class Newbidemail(generics.RetrieveAPIView):
    serializer_class = BidSerializerBasic

    def get_queryset(self):
        bid_id = self.kwargs['pk']
        currentbid = Bid.objects.get(id=bid_id)
        subject = 'New bid placed recieved for your project'
        html_message = render_to_string('emails/newbid.html',{'bid': currentbid})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = currentbid.project.client.user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Bid.objects.all()

class Acceptbidemail(generics.RetrieveAPIView):
    serializer_class = BidSerializerBasic

    def get_queryset(self):
        bid_id = self.kwargs['pk']
        currentbid = Bid.objects.get(id=bid_id)
        subject = 'Your bid has been accepted'
        html_message = render_to_string('emails/acceptedbid.html',{'bid': currentbid})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = currentbid.developer.user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Bid.objects.all()

class ProjectBidsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializerBasic

    def get_queryset(self):

        return Bid.objects.filter(project__slug__iexact=self.kwargs['project_slug']).exclude(withdraw=True)

class DeveloperBidsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializer

    def get_queryset(self):

        return Bid.objects.filter(developer__pk =self.kwargs['developer_id']).exclude(withdraw=True)
class AcceptedDeveloperBidsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BidSerializer

    def get_queryset(self):

        return Bid.objects.filter(developer__pk =self.kwargs['developer_id']).exclude(withdraw=True).exclude(accepted=True)
class AcceptBidView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoteDeveloperSerializer

    def get_queryset(self):
        return RemoteDeveloper.objects.all()

# tasks

class CreateTaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializerUpdater

    def get_queryset(self):
        return Tasks.objects.all()

class FeatureTasksGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Tasks.objects.filter(feature__pk = self.kwargs['feature_id'])

class FeatureTaskUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializerUpdater

class FeatureTaskDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializerUpdater
    def get_queryset(self):
        instance = Tasks.objects.get(pk = self.kwargs['pk'])
        instance.delete()
        return Tasks.objects.all()

# issue

class CreateIssueView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

class AllIssuesGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializerDetail

    def get_queryset(self):
        posted = Profile.objects.get(pk = self.kwargs['owner_id'])
        if posted.user.is_staff:
            return Issue.objects.all()
        else:
            return Issue.objects.filter(feature__project__posted_by=self.kwargs['owner_id'])


class AllIssuesDeveloperGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializerDetail

    def get_queryset(self):
        return Issue.objects.filter(feature__project__assigned_to=self.kwargs['assigned_to'])

class FeatureIssueGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(feature__pk = self.kwargs['feature_id'])

class FeatureIssueUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class FeatureIssueDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = IssueSerializer
    def get_queryset(self):
        instance = Issue.objects.get(pk = self.kwargs['pk'])
        instance.delete()
        return Issue.objects.all()

# comment

class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializerBasic

    def get_queryset(self):
        return Comments.objects.all()

class IssueCommentsGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.filter(issue__pk = self.kwargs['issue_id'])

#teams
class CreateTeamView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.all()

class MyTeamsGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.filter(lead__pk = self.kwargs['leader_id'] )

class TeamUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamUserget(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'email'
    serializer_class = UserSerializer
# files upload
class CreateFileEntryView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FilesSerializer

    def get_queryset(self):
        return Files.objects.all()

class ProjectFilesGet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FilesSerializer

    def get_queryset(self):
        return Files.objects.filter(project__pk =self.kwargs['project_id'] )

class ProjectFilesUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

class CreateContractView(generics.CreateAPIView):
    pass


class ContractsListView(generics.ListAPIView):
    pass


class CreatePaymentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    pass


class PaymentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    pass
