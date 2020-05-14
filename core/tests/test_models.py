from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import Size, Item, StockItem, OrderItem, Order
from users.models import User
from core.tests.factories import (
    SizeFactory,
    ItemFactory,
    StockItemFactory,
    OrderItemFactory,
    OrderFactory
)
from users.tests.factories import UserFactory, AddressFactory


class SizeModelTest(TestCase):
    def test_size_name(self):
        size = SizeFactory(name='S')
        self.assertEquals('S', str(size))


class ItemModelTest(TestCase):
    def setUp(self):
        self.item1 = Item.objects.create(name='item1', category='C1', price=56)
        self.item2 = Item.objects.create(name='item2', category='C1', price=25)

        StockItem.objects.create(stock=1, item=self.item1)
        StockItem.objects.create(stock=0, item=self.item2)

    def test_item_name(self):
        item = Item.objects.get(name='item1')
        expected_item_name = self.item1.name
        self.assertEqual(expected_item_name, str(item))

    def test_in_stock(self):
        self.assertTrue(self.item1.in_stock())
        self.assertFalse(self.item2.in_stock())

    def test_discount_price_cant_be_bigger_then_price(self):
        self.item2 = Item.objects.create(name='item2', price=100, discount_price=120)
        # Check that a ValidationError is raised
        self.assertRaises(ValidationError, self.item2.clean)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='1234')
        self.size_s = Size.objects.create(name='S')
        self.item1 = Item.objects.create(name='item1', price=100, discount_price=90)
        self.order_item1 = OrderItem.objects.create(
            user=self.user1, item=self.item1, size=self.size_s, quantity=5
        )
        self.item2 = Item.objects.create(name='item2', price=100)
        self.order_item2 = OrderItem.objects.create(
            user=self.user1, item=self.item2, size=self.size_s, quantity=5
        )

    def test_order_item_name(self):
        order_item1 = OrderItem.objects.get(user=self.user1, item=self.item1, size=self.size_s)
        expected_order_item1_name = f'OrderItem of {self.item1.name}'
        self.assertEqual(expected_order_item1_name, str(order_item1))

    def test_total_item_price(self):
        total = self.order_item1.total_item_price()
        self.assertEqual(total, 500)

    def test_total_discount_price(self):
        total_discount = self.order_item1.total_discount_item_price()
        self.assertEqual(total_discount, 450)

    def test_amount_saved(self):
        amount_saved = self.order_item1.amount_saved()
        self.assertEqual(amount_saved, 50)

    def test_final_price(self):
        final_price1 = self.order_item1.final_price()
        # Check that 'final_price' is equal to 'total_discount_item_price'
        self.assertEqual(final_price1, self.order_item1.total_discount_item_price())

        final_price2 = self.order_item2.final_price()
        # Check that 'final_price' is equal to 'total_item_price'
        # since we don't have a discount price
        self.assertEqual(final_price2, self.order_item2.total_item_price())


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order = OrderFactory(user=self.user)

    def test_factory(self):
        order = OrderFactory(user=self.user)

        self.assertIsNotNone(order)
        self.assertIsNone(order.shipping_address)

    def test_order_name(self):
        expected_order_name = f'Order of user {self.user.username}'

        self.assertEqual(expected_order_name, str(self.order))

    def tes_has_user(self):
        self.assertEqual(user, self.order.user)