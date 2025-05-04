from django.core.mail import send_mail
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def send_test_email(self):
        try:
            send_mail(
                'Subject here',
                'Here is the message.',
                settings.EMAIL_HOST_USER,
                ['linoy7000@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(e)

    def handle(self, *args, **options):
        self.send_test_email()
