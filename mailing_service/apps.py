# mailing_service/apps.py
from django.apps import AppConfig


class MailingServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_service'

    def ready(self):
        pass
