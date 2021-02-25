from django.urls import path
from account_manager.views import index

app_name = 'account_manager'

urlpatterns = [
    path('', index)
]