# mailing_service/utils.py
from django.core.mail import send_mail


class EmailSender:
    def __init__(self, subject, message, from_email, recipient_list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list

    def send(self):
        send_mail(
            self.subject,
            self.message,
            self.from_email,
            self.recipient_list,
            fail_silently=False,
        )
