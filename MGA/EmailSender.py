from django.core.mail import send_mail


class EmailSender:

    @staticmethod
    def send_email(email,message,subject):
        send_mail(
            subject,
            message,
            'z.y.j.1379@gmail.com',
            [email],
            fail_silently=False,
        )
