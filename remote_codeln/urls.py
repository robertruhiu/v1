from django.urls import path, include
from remote_codeln import views

app_name = 'remote_codeln'

urlpatterns = [
    path('v1/', include([
        path('projects/', include([
            path('create/', views.CreateProjectView.as_view()),
            path('getproject/<int:pk>', views.GetProject.as_view()),
            path('getprojectslug/<slug:slug>', views.GetProjectSlug.as_view()),
            path('updateproject/<int:pk>', views.ProjectUpdate.as_view()),
            path('all/', views.ProjectListView.as_view()),
            path('myprojects/<int:owner>', views.ProjectOwnerListView.as_view()),

            path('developerprojects/<int:assigned_to>', views.ProjectDeveloperListView.as_view()),
            path('<slug:slug>/', views.ProjectListView.as_view()),
            # TODO: view for single project view
            path('features/', include([
                path('create/', views.CreateFeatureView.as_view()),
                # TODO: view for single bid view
                path('getprojectfeatures/<int:pk>', views.ProjectFeatureGet.as_view()),
                path('getfeature/<int:pk>', views.FeatureGet.as_view()),
                path('update/<int:pk>', views.ProjectFeatureUpdate.as_view()),
                path('deletefeature/<int:pk>', views.ProjectFeatureDelete.as_view()),
                path('finishedfeature/<int:pk>', views.FinishedFeature.as_view()),

            ])),
            path('stories/', include([
                path('create/', views.CreateStoriesView.as_view()),
                # TODO: view for single bid view
                path('getfeaturestories/<int:pk>', views.FeatureStoryGet.as_view()),
                path('update/<int:pk>', views.FeatureStoryUpdate.as_view()),
                path('deletestory/<int:pk>', views.FeatureStoryDelete.as_view()),

            ])),
            path('bids/', include([
                path('create/', views.CreateBidView.as_view()),
                # TODO: view for single bid view
                path('projectbids/<str:project_slug>', views.ProjectBidsListView.as_view()),
                path('developerbids/<int:developer_id>', views.DeveloperBidsListView.as_view()),
                path('activedeveloperbids/<int:developer_id>', views.AcceptedDeveloperBidsListView.as_view()),
                path('updatebid/<int:pk>', views.BidUpdateView.as_view()),
                path('acceptbid/', views.AcceptBidView.as_view()),
                path('newbidemail/<int:pk>', views.Newbidemail.as_view()),
                path('acceptedbidemail/<int:pk>', views.Acceptbidemail.as_view()),

            ])),
            path('tasks/', include([
                path('create/', views.CreateTaskView.as_view()),
                path('featuretasks/<str:feature_id>', views.FeatureTasksGet.as_view()),
                path('updatetask/<int:pk>', views.FeatureTaskUpdate.as_view()),
                path('deletetask/<int:pk>', views.FeatureTaskDelete.as_view()),

            ])),
            path('issues/', include([
                path('create/', views.CreateIssueView.as_view()),
                path('featureissues/<int:feature_id>', views.FeatureIssueGet.as_view()),
                path('allissues/<int:owner_id>', views.AllIssuesGet.as_view()),
                path('developerallissues/<int:assigned_to>', views.AllIssuesDeveloperGet.as_view()),
                path('updateissue/<int:pk>', views.FeatureIssueUpdate.as_view()),
                path('deleteissue/<int:pk>', views.FeatureIssueDelete.as_view()),

            ])),
            path('comments/', include([
                path('create/', views.CreateCommentView.as_view()),
                path('issuecomments/<int:issue_id>', views.IssueCommentsGet.as_view()),

            ])),
            path('teams/', include([
                path('create/', views.CreateTeamView.as_view()),
                path('myteams/<int:leader_id>', views.MyTeamsGet.as_view()),
                path('updateteam/<int:pk>', views.TeamUpdate.as_view()),
                path('getuser/<str:email>', views.TeamUserget.as_view())

            ])),
            path('files/', include([
                path('create/', views.CreateFileEntryView.as_view()),
                path('fetchfiles/<int:project_id>', views.ProjectFilesGet.as_view()),
                path('updatefile/<int:pk>', views.ProjectFilesUpdate.as_view()),

            ])),
            path('signatures/', include([
                path('create/', views.CreateSignatureEntryView.as_view()),
                path('fetchsignature/<int:owner>', views.SignatureGet.as_view()),
                path('updatesignature/<int:pk>', views.SignatureUpdate.as_view()),

            ])),
            path('contract/', include([
                path('create/', views.CreateContractView.as_view()),
                # TODO: view for single contract view
                path('all/', views.ContractsListView.as_view()),
            ])),
            path('issues/', include([
                path('create/', views.CreateContractView.as_view()),
                # TODO: view for single issue view
                path('all/', views.ContractsListView.as_view()),
            ])),

            path('payments/', include([
                path('create/', views.CreatePaymentView.as_view()),
                # TODO: view for single issue view
                path('get/<int:project>', views.PaymentGet.as_view()),
            ])),
            path('chat/', include([
                path('all/<str:user>', views.ChatGet.as_view()),
                # path('all/<str:user>', views.chats, name='chats'),
                path('with/<str:user>/<str:other_user>', views.chat_with, name='with'),
                path('send_message/<str:user>/<str:other_user>/<str:channel_url>', views.send_message, name='chat_message'),
                path('send_message2/<str:user>/<str:other_user>/<str:channel_url>/<str:message>', views.send_message2, name='chat_message'),
            ])),
        ])),
    ])),
]
