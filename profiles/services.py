from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


def send(user_mail):
    send_mail('Send Hello', 'You are login on our site', EMAIL_HOST_USER, [user_mail], fail_silently=False)
