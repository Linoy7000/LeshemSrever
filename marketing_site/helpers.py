import random
import string

from django.conf import settings
from django.core.mail import send_mail

def generate_otp_code():
    return ''.join(random.choices(string.digits, k=6))

def send_email(subject, message, addressee):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [addressee],
        fail_silently=False
    )