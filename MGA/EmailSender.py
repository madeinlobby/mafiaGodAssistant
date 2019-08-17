from django.core.mail import send_mail

from mafiaGodAssistant import settings


class EmailSender:

    @staticmethod
    def send_email(email,message,subject):
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
