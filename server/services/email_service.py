
from django.core.mail import EmailMessage


class EmailService:

    def send_email(self, receipts, subject, body, attachment=None):
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=receipts,
            )
            if attachment:
                email.attach("pdf_name.pdf", attachment, "application/pdf")
            email.send()
        except Exception as e:
            return "Error"

from django.core.mail import send_mail
from django.conf import settings

def send_test_email():
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['linoy7000@gmail.com'],
        fail_silently=False,
    )