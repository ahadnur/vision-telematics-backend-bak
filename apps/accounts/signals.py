from django.db.models.signals import post_save
from apps.accounts.models import User, Profile
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)



