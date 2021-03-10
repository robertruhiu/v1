from django.urls import path
from account_manager import views

app_name = 'account_manager'
#
urlpatterns = [
    path('', views.index, name='base'),
    # path('devs/', views.index),
    path('jobs/', views.jobs, name='jobs'),
    path('myjob/<int:id>/', views.myjob, name='myjob'),
    path('update_application/', views.update_application, name='update_application'),
    # path('devs/', views.devs, name='devs'),
    path('mydev/<int:id>/', views.mydev, name='mydev'),
    path('all_shortlist/', views.all_shortlist, name='all_shortlist'),
    path('shortlist/<int:id>/', views.shortlist, name='shortlist'),
    path('add_to_list/<int:id>/', views.add_to_list, name='add_to_list'),
    path('send_mail/<int:id>/', views.add_to_list, name='send_mail'),
    path('shortlist/create/', views.ShortlistCreate.as_view(), name='shortlist_create'),
    path('shortlist/<int:pk>/update/', views.ShortlistUpdate.as_view(), name='shortlist_update'),
    path('shortlist/<int:pk>/delete/', views.ShortlistDelete.as_view(), name='shortlist_delete'),
    path('cv/', views.cv, name='cv'),
    path('download_cv/', views.download_cv, name='download_cv'),
    # path('test/', views.GeneratePdf.as_view(), name='download_cv'),
]