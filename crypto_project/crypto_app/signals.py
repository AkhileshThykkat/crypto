from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Organisation
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Organisation)
def log_organization_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New organization created: {instance.name} by {instance.owner}")

@receiver(post_delete, sender=Organisation)
def log_organization_deleted(sender, instance, **kwargs):
    logger.info(f"Organization deleted: {instance.name} by {instance.owner}")
