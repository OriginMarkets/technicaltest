import logging
import uuid
from typing import Any, Dict

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(
    sender: models.Model, instance: Any = None, created: bool = False, **kwargs: Dict
) -> None:
    if created:
        logger.debug("Creating user token post user creation")
        Token.objects.create(user=instance)


class LegalEntity(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    legal_name = models.CharField(max_length=128)
    lei = models.CharField(max_length=128)


class Bond(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    isin = models.CharField(max_length=12)
    size = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    # Just because we delete a bond doesn't mean we should delete the referenced Legal Entity.
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.PROTECT)

    class Meta:
        # An International Securities Identification Number (ISIN) uniquely identifies a security
        # so make a constraint against the user to prevent duplicate isin entries.
        constraints = [models.UniqueConstraint(fields=["isin", "user"], name="unique_isin")]
