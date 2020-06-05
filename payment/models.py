from django.db import models
from django.conf import settings

from core.models import Order


class StripePayment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='customer',
        blank=True,
        null=True
    )
    order = models.OneToOneField(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=50, blank=True, null=True)
