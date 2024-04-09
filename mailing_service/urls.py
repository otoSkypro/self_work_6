# mailing_service/urls.py
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import (
    SentMailingsReportView,
    send_test_email_view,
    ClientDeleteConfirmationView,
    ClientDeleteView,
    ClientCreateView,
    ClientUpdateView,
    ClientListView,
    MailingListView,
    MailingCreateView,
    MailingUnblockView,
    MailingBlockView,
    MailingUpdateView,
    MailingDeleteView,
    MailingDetailView,
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    LogListView,
    HomeView,
)

app_name = 'mailing_service'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logs/', LogListView.as_view(), name='log_list'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/delete-confirm/<str:selected_clients>/', ClientDeleteConfirmationView.as_view(),
         name='client_confirm_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/block/', MailingBlockView.as_view(), name='mailing_block'),
    path('mailings/<int:pk>/unblock/', MailingUnblockView.as_view(), name='mailing_unblock'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('sent-mailings-report/', SentMailingsReportView.as_view(), name='sent_mailings_report'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('send-test-email/', send_test_email_view, name='send_test_email'),
]

# Обернем все URL-пути, кроме 'home' и 'blog', декоратором login_required
for urlpattern in urlpatterns:
    if urlpattern.name not in ['home', 'blog']:  # Исключаем 'home' и 'blog'
        urlpattern.callback = login_required(urlpattern.callback)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
