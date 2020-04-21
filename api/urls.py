from django.urls import path

from api.views import EnterpriseProjects, schedule_test, developer_report, AllReports, enterprise_test_complete, \
    enterprise_report_ready, ScheduledTests, TakenTests

app_name = "api"

urlpatterns = [
    path('projects/', EnterpriseProjects.as_view()),
    # path('schedule_test/', schedule_test, name='schedule_test'),
    path('scheduledtests/', ScheduledTests.as_view()),
    path('takentests/', TakenTests.as_view()),
    path('report/', developer_report, name='developer_report'),
    path('allreports/', AllReports.as_view()),
    path('enterprise_test_complete/<int:id>/', enterprise_test_complete),
    path('enterprise_report_ready/<int:id>/', enterprise_report_ready),

]
