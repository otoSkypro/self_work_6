# mailing_service/views.py

from django.shortcuts import render


def home(request):
    return render(request, 'mailing_service/home.html')


def mailing_list_view(request):
    return render(request, 'mailing_service/mailing_list_list.html')


def log_list(request):
    return render(request, 'mailing_service/log_list.html')
