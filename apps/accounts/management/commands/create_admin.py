import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db import transaction

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creating for admin"

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of superuser')
        parser.add_argument('password1', type=str, help='Enter your password')
        parser.add_argument('password2', type=str, help='Confirm your password')

    def handle(self, *args, **kwargs):
        email = kwargs.get('email')
        password1 = kwargs.get('password1')
        password2 = kwargs.get('password2')

        user = get_user_model()
        try:
            if user.objects.filter(email=email).exists():
                logger.error(f'Email {email} already exists')
                return
            else:
                if password1 != password2:
                    logger.error(f'Passwords do not match')
                else:
                    user.is_superuser = True
                    user.is_staff = True
                    user.is_active = False
                    user.save()
                    self.send_verification_email(user)
                    logger.info(f"Successfully created superuser {email} & verification email sent.")
        except Exception as e:
            logging.error(str(e))
            return

    @staticmethod
    def send_verification_email(self, user):
        token = get_random_string(30)
        user.verification_token = token
        user.save()

        # prepare email data
        current_site = get_current_site(None)
        mail_subject = 'Activate your account'
        message = render_to_string('accounts/email/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })

        send_mail(
            mail_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
        logger.info(f'Email verification sent to {user.email}')

