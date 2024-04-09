# mailing_service/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from Django_Spam_Service_2024 import settings
from .models import Mailing, Message, Log
from django.utils import timezone
from .utils import EmailSender

# Создаем экземпляр планировщика задач APScheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


class EmailTask:
    @classmethod
    def start(cls):
        scheduler.start()

    @classmethod
    def send_emails(cls, mailing_id):
        current_time = timezone.now()
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            if mailing.start_time <= current_time <= mailing.end_time:
                for client in mailing.clients.all():
                    message = Message.objects.create(mailing=mailing, subject=mailing.title, body=mailing.content)
                    email_sender = EmailSender(
                        subject=message.subject,
                        message=message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email]
                    )
                    try:
                        email_sender.send()
                        log = Log.objects.create(message=message, attempt_time=current_time,
                                                 status='Сообщение отправлено успешно')
                    except Exception as e:
                        log = Log.objects.create(message=message, attempt_time=current_time,
                                                 status='Ошибка при отправке сообщения', response=str(e))
        except Mailing.DoesNotExist:
            pass

    @classmethod
    def stop(cls):
        scheduler.shutdown()


scheduler.add_job(EmailTask.send_emails, 'interval', minutes=1, args=['mailing_id'])
