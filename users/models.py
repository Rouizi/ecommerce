from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    """A custom user for extension"""
    pass


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255, null=True)
    billing_address = models.CharField(max_length=255, null=True)
    shipping_zip = models.CharField(max_length=50, null=True)
    billing_zip = models.CharField(max_length=50, null=True)
    default_shipping_address = models.BooleanField(default=False)
    default_billing_address = models.BooleanField(default=False)

    def __str__(self):
        return f'Address of user {self.user.username}'

    class Meta:
        verbose_name_plural = 'Addresses'
