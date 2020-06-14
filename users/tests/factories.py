import factory, factory.fuzzy

from django.conf import settings
from users import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.PostGenerationMethodCall('set_password', '1234')


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Address

    shipping_address = factory.Sequence(lambda n: 'shipping_address_%d' % n)
    billing_address = factory.Sequence(lambda n: 'billing_address_%d' % n)
    shipping_zip = factory.Sequence(lambda n: 'shipping_zip_%d' % n)
    billing_zip = factory.Sequence(lambda n: 'billing_zip_%d' % n)
