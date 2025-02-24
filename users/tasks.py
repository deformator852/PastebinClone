from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import force_bytes


@shared_task
def send_verification_email(username) -> None:
    current_site = Site.objects.get(id=settings.SITE_ID)
    user = User.objects.get(username=username)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_url = f"http://{current_site.domain}{reverse('verify_email', kwargs={'uidb64': uid, 'token': token})}"
    message = f"""
    Hi {user.username}!
    Please confirm your email by clicking the link below:
    {verification_url}
    """
    email = EmailMessage("Verify email", message, to=[user.email])
    email.send()
