from django.urls import path

from api.views import EnterpriseProjects, schedule_test, developer_report, AllReports, enterprise_test_complete, \
    enterprise_report_ready, ScheduledTests, TakenTests, create_ide_user, get_project, create_report

app_name = "api"

urlpatterns = [
    path('projects/', EnterpriseProjects.as_view()),
    path('schedule_test/', schedule_test, name='schedule_test'),
    path('scheduledtests/', ScheduledTests.as_view()),
    path('takentests/', TakenTests.as_view()),
    path('report/', developer_report, name='developer_report'),
    path('allreports/', AllReports.as_view()),
    path('enterprise_test_complete/<slug:slug>/', enterprise_test_complete),
    path('create_report/<slug:slug>/', create_report),
    path('enterprise_report_ready/<slug:slug>/', enterprise_report_ready),
    path('testuser/', create_ide_user, name='create_ide_user'),
    path('get_project/<slug:slug>/', get_project, name='get_project'),
]
