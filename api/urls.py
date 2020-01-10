from django.urls import path

from api.views import EnterpriseProjects, schedule_test, developer_report, AllReports

app_name = "api"

urlpatterns = [
    path('projects/', EnterpriseProjects.as_view()),
    path('schedule_test/', schedule_test, name='schedule_test'),
    path('report/', developer_report, name='developer_report'),
    path('allreports/', AllReports.as_view()),

]
