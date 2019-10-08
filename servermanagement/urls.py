"""codetest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from servermanagement.views import schedule_job, JobDetailView, test_widgets, test_create_server, \
    report, AssessmentDetail, manual_test, automated_test, TestCenterList

# , EnterpriseScheduleJob, \
    # EnterpriseProjectsDetail, EnterpriseCandidateDetail, EnterpriseCandidateProjectsDetail, \
    # EnterpriseCandidateSetUpDetail, EnterpriseScheduleDemoJob, candidate_pending, EnterpriseCandidateEmail

# EnterpriseCandidateList

app_name = 'servermanagement'

urlpatterns = [
    # path('schedule_job/<int:project_id>/', schedule_job, name='schedule-job'),
    path('job-detail/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('test-create/', test_create_server, name='test-create'),
    path('report/', report, name='report'),

]

urlpatterns += [
    # path('test_form/', test_widgets, name='test-form'),
    # path('approve_test/<int:pk>/', AssessmentDetail.as_view(), name='approve_test'),
    path('test_centers/', TestCenterList.as_view(), name='test_centers'),
    path('automated_test/<int:pk>/', automated_test, name='automated_test'),
    path('manual_test/', manual_test.as_view()),
]

# enterprise urls
# urlpatterns += [
#     path('candidate_create/', EnterpriseCandidateDetail.as_view(), name='candidate_create'),
#     path('schedule_test/', EnterpriseScheduleJob.as_view(), name="schedule_test"),
#     path('schedule_test_demo/', EnterpriseScheduleDemoJob.as_view(), name="schedule_test_demo"),
#     path('enterprise_projects/', EnterpriseProjectsDetail.as_view(), name='enterprise_projects'),
#     path('enterprise_candidates/', EnterpriseCandidateProjectsDetail.as_view(), name='enterprise_candidates'),
#     path('enterprise_candidate_setup/', EnterpriseCandidateSetUpDetail.as_view(), name='enterprise_candidate_setup'),
#     path('enterprise_candidate_email/',EnterpriseCandidateEmail.as_view(), name='enterprise_candidate_email'),
#     # path('enterprise_candidate_setup/',EnterpriseCandidateSetUpDetail.as_view(), name='enterprise_candidate_setup'),
#     # re_path(r'enterprise_projects$', EnterpriseProjectsList.as_view(), name= 'enterprise_projects'),
#
# ]

# demo paths
# from servermanagement.views import candidate_list, candidate_tested, js_tested, python_tested, js_pending, python_pending,\
#     allreports, finish_project
#
# urlpatterns += [
#     path('candidate_list/', candidate_list, name="candidate_list"),
#     path('candidate_tested/', candidate_tested, name="candidate_tested"),
#     path('candidate_pending/', candidate_pending, name="candidate_pending"),
#     path('candidate_pending/', candidate_pending, name="candidate_pending"),
#     path('js_tested/', js_tested, name="js_tested"),
#     path('js_pending/', js_pending, name="js_pending"),
#     path('python_tested/', python_tested, name="python_tested"),
#     path('python_pending/', python_pending, name="python_pending"),
#     path('all_reports/', allreports, name="allreports"),
#     path('uncomplete/', finish_project, name="uncomplete"),
# #
# ]
