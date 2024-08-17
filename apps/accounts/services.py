from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from rest_framework.exceptions import NotFound

from .models import Account
from .models.user import User
import logging

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, email_service=None):
        self.user = User
        self.email_service = email_service

    def get_user(self, _id):
        return self.user.objects.filter(id=_id).first()


class AccountService:
    def __init__(self, email_service=None):
        pass

    @staticmethod
    def get_account(_id):
        try:
            return Account.objects.filter(id=_id).first()
        except Account.DoesNotExist:
            raise NotFound(detail="Account not found")


class EmailVerificationService:
    def __init__(self, request):
        self.request = request
        self.user = User

    def send_verification_email(self, user):
        token = get_random_string(30)
        user.verification_token = token
        user.save()

        current_site = get_current_site(self.request)
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

