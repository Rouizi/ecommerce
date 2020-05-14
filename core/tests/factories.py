import factory, factory.fuzzy

from core import models
from users.tests.factories import UserFactory


class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Size


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Item

    name = factory.Sequence(lambda n: 'item_%d' % n)
    category = factory.fuzzy.FuzzyChoice(models.Item.CATEGORY, getter=lambda c: c[0])
    label = factory.fuzzy.FuzzyChoice(models.Item.LABEL, getter=lambda c: c[0])
    color_label = factory.fuzzy.FuzzyChoice(models.Item.COLOR_LABEL, getter=lambda c: c[0])
    price = factory.Sequence(lambda n: (n + 1))
    description = factory.Faker('sentence')
    image1 = 'image1'
    slug = factory.LazyAttribute(lambda o: o.name)


class StockItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.StockItem

    stock = 1
    item = factory.SubFactory(ItemFactory)
    size = factory.SubFactory(SizeFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    user = factory.SubFactory(UserFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrderItem

    user = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
    order = factory.SubFactory(OrderFactory)

