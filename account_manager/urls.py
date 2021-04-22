from django.urls import path
from account_manager import views

app_name = 'account_manager'
#
urlpatterns = [
    path('', views.index, name='base'),
    path('jobs/', views.jobs, name='jobs'),
    path('myjob/<int:id>/', views.myjob, name='myjob'),
    path('update_application/', views.update_application, name='update_application'),
    path('mydev/<int:id>/', views.mydev, name='mydev'),
    path('all_shortlist/', views.all_shortlist, name='all_shortlist'),
    path('shortlist/<int:id>/', views.shortlist, name='shortlist'),
    path('add_to_list/<int:id>/', views.add_to_list, name='add_to_list'),
    path('remove_dev/<int:shortlist_id>/<int:dev_id>/', views.remove_dev, name='remove_dev'),
    path('send_email/<int:id>/', views.send_email, name='send_email'),
    path('invite_to_job/<int:id>/', views.invitetojob, name='invite_to_job'),
    path('shortlist/create/', views.ShortlistCreate.as_view(), name='shortlist_create'),
    path('shortlist/<int:pk>/update/', views.ShortlistUpdate.as_view(), name='shortlist_update'),
    path('shortlist/<int:pk>/delete/', views.ShortlistDelete.as_view(), name='shortlist_delete'),
    path('cv/<int:id>/', views.cv, name='cv'),
    path('download_cv/<int:id>/', views.download_cv, name='download_cv'),
    path('download_stripped_cv/<int:id>/', views.download_stripped_cv, name='download_stripped_cv'),
]