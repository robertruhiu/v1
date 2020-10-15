from django.urls import path, include
from remote_codeln import views

app_name = 'remote_codeln'

urlpatterns = [
    path('v1/', include([
        path('projects/', include([
            path('create/', views.CreateProjectView.as_view()),
            path('all/', views.ProjectListView.as_view()),
            path('<slug:slug>/', views.ProjectListView.as_view()),
            # TODO: view for single project view
            path('bids/', include([
                path('create/', views.CreateBidView.as_view()),
                # TODO: view for single bid view
                path('all/', views.BidsListView.as_view()),
                path('update/', views.BidView.as_view()),

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
                path('all/', views.PaymentListView.as_view()),
            ])),
        ])),
    ])),
]
