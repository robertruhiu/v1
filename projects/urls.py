"""codelnmain URL Configuration

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
from projects.views import project_list, project, categories, devtypes, Projects \
    , ProjectDetails, Allprojects, RecentProjects, MyRecentProjects, RecommendedProjects, \
    DeveloperProjects, developerprojectreport, Frameworks, SelfverifyProject, BasicProject, clidext, clidextupdate

app_name = 'projects'
urlpatterns = [
    # path('', project_categories, name='categories'y),
    path('all-projects/<int:type_id>/', project_list, name='all-projects'),
    path('devtypes/<int:dev_id>/', devtypes, name='devtypes'),
    path('categories/', categories, name='categories'),
    path('project/<int:id>/', project, name='project'),
    path('projects/<int:id>', Projects.as_view()),
    path('recommendedprojects/<int:id>', RecommendedProjects.as_view()),
    path('selfverifyproject/<int:dev_id>/<str:framework>', SelfverifyProject.as_view()),
    path('basicproject/<int:dev_id>/<str:framework>', BasicProject.as_view()),
    path('allprojects', Allprojects.as_view()),
    path('projectdetails/<int:pk>', ProjectDetails.as_view()),
    path('recentprojects/<int:id>', RecentProjects.as_view()),
    path('myrecentprojects/<int:id>', MyRecentProjects.as_view()),

]

# developer api views
urlpatterns += [
    path('developerprojects/<str:framework>', DeveloperProjects.as_view()),
    path('developerprojectreport/<int:candidate_id>/<int:project_id>/',
         developerprojectreport, name='developerprojectreport'),
    path('frameworks', Frameworks.as_view()),
]
# developer api views
urlpatterns += [
    path('clidext/<str:email>/', clidext, name='clidext'),
    path('clideupdate/<str:email>/<int:id>/', clidextupdate, name='clideupdate'),
]
#
# from django.views.generic import TemplateView
#
# urlpatterns += [
#     path('testgame/', TemplateView.as_view(template_name="projects/testgame.html"),
#          name='testgame'),
# ]
