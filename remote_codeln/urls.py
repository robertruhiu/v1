from django.urls import path, include
from remote_codeln import views

app_name = 'remote_codeln'

urlpatterns = [
    path('v1/', include([
        path('projects/', include([
            path('create/',views.CreateProject.as_view()),
        ])),
    ]),
]