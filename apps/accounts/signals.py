from django.db.models.signals import post_save
from apps.accounts.models import User, Profile
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        logger.debug(f'Creating profile for user: {instance}')
        Profile.objects.create(user=instance)
