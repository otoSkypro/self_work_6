# mailing_service/urls.py
from django.urls import path
from . import views

app_name = 'mailing_service'

urlpatterns = [
    path('', views.home, name='home'),
    path('logs/', views.log_list, name='log_list'),
    path('mailing_list/', views.mailing_list_view, name='mailing_list_list'),
    path('client_list/', views.mailing_list_view, name='client_list'),
]
