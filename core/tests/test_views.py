from django.test import TestCase
from django.urls import reverse

from core.models import Size, Item, StockItem, OrderItem, Order
from users.models import User, Address
from core.tests.factories import (
    ItemFactory,
    SizeFactory,
    StockItemFactory,
    OrderFactory,
    OrderItemFactory
)
from users.tests.factories import UserFactory, AddressFactory


class HomeViewTest(TestCase):
    # I am not going to test this view because
    # I tested somthing like this in my OC_project13
    pass


class ItemDetailViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='1234')
        self.user2 = User.objects.create_user(username='user2', password='1234')

        self.size_s = Size.objects.create(name='S')
        self.size_m = Size.objects.create(name='M')

        self.item1 = Item.objects.create(
            name='item1', price=100, image1='img1', image2='img2', slug='item1')
        self.item2 = Item.objects.create(
            name='item2', price=100, image1='img1', image2='img2', slug='item2')
        self.item3 = Item.objects.create(
            name='item3', price=100, image1='img1', image2='img2', slug='item3')

        StockItem.objects.create(stock=0, item=self.item1, size=self.size_s)
        StockItem.objects.create(stock=5, item=self.item2, size=self.size_s)
        StockItem.objects.create(stock=5, item=self.item3, size=self.size_s)

        OrderItem.objects.create(
            user=self.user1, item=self.item1, size=self.size_s, quantity=5)
        OrderItem.objects.create(
            user=self.user1, item=self.item2, size=self.size_s, quantity=1)

        self.pk1 = self.item1.pk
        self.slug1 = self.item1.slug
        self.pk2 = self.item2.pk
        self.slug2 = self.item2.slug
        self.pk3 = self.item3.pk
        self.slug3 = self.item3.slug

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(
            'core:product', kwargs=({'pk': self.pk1, 'slug': self.slug1}))
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/product.html')

    def test_redirect_if_post_whitout_login(self):
        """Test that only logged in user can send a post request"""
        response = self.client.post(
            reverse('core:product', kwargs=({'pk': self.pk1, 'slug': self.slug1})),
            {
                'size': 'S',
                'quantity': 10
            }
        )
        # Check user are redirected to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/product/' + str(self.pk1) + '/item1/')

    def test_max_quantity_of_item_allowed(self):
        """Test that users cannot order more than 20 identical products"""
        login = self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:product', kwargs=({'pk': self.pk1, 'slug': self.slug1})),
            {
                'size': 'S',
                'quantity': 16
            }
        )
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'You cannot add more than 20 identical products to the cart.')

    def test_out_of_stock(self):
        login = self.client.login(username='user1', password='1234')
        print(login)
        response = self.client.post(
            reverse('core:product', kwargs=({'pk': self.pk1, 'slug': self.slug1})),
            {
                'size': 'S',
                'quantity': 1
            }
        )
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This product is out of stock for SMALL size.')

    def test_stock_limited(self):
        """
        Test that the view returns an error message if the
        stock is lower then the quantity the user requested for
        """
        login = self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:product', kwargs=({'pk': self.pk2, 'slug': self.slug2})),
            {
                'size': 'S',
                'quantity': 6
            }
        )
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'There are only 5 product(s) of this size in stock.')

    def test_item_not_available_for_size(self):
        """
        Test that the view returns an error message
        if the item is unavailable for the size the user requested
        """
        login = self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:product', kwargs=({'pk': self.pk1, 'slug': self.slug1})),
            {
                'size': 'M',
                'quantity': 1
            }
        )
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This item is unavailable for this size.')

    def test_add_to_cart_with_order_item(self):
        """Test the add_to_cart function if a user has an order item"""
        stock_before = StockItem.objects.get(item=self.item2).stock  # The stock before the request
        # The quantity before the request
        quantity_before = OrderItem.objects.get(
            user=self.user1,
            item=self.item2,
            size=self.size_s,
            ordered=False
        ).quantity
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:product', kwargs={'pk': self.pk2, 'slug': self.slug2}),
            {
                'size': 'S',
                'quantity': 3
            }
        )
        stock_after = StockItem.objects.get(item=self.item2).stock  # The stock after the request
        # The quantity after the request
        quantity_after = OrderItem.objects.get(
            user=self.user1,
            item=self.item2,
            size=self.size_s,
            ordered=False
        ).quantity

        # Check that stock decreased by 3
        self.assertEqual(stock_after, stock_before - 3)
        # Check that quantity of order item increased by 3
        self.assertEqual(quantity_after, quantity_before + 3)
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This item quantity for size S was updated.')

    def test_add_to_cart_without_order_item(self):
        """Test add_to_cart function if a user has not an order item"""
        self.client.login(username='user2', password='1234')
        order_item2_user2 = OrderItem.objects.filter(
            user=self.user2,
            item=self.item2,
            size=self.size_s,
            ordered=False
        )
        order_user2 = Order.objects.filter(user=self.user2, ordered=False)

        # Check that user2 has not an order item before the request
        self.assertFalse(order_item2_user2.exists())
        # Check that user2 has not an order before the request
        self.assertFalse(order_user2.exists())

        response = self.client.post(
            reverse('core:product', kwargs={'pk': self.pk2, 'slug': self.slug2}),
            {
                'size': 'S',
                'quantity': 3
            }
        )

        # Check that an order was created for user2
        self.assertTrue(order_user2.exists())
        # Check that an order item was created for user2
        self.assertTrue(order_item2_user2.exists())
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This item for size S was added to your cart.')

        # Now we check that a new order item is added to the order
        order_item3_user2 = OrderItem.objects.filter(
            user=self.user2,
            item=self.item3,
            size=self.size_s,
            order=order_user2[0],
            ordered=False
        )

        # Check that order_item3_user2 does not belong to order_user2 before the request
        self.assertFalse(order_item3_user2.exists())

        response = self.client.post(
            reverse('core:product', kwargs={'pk': self.pk3, 'slug': self.slug3}),
            {
                'size': 'S',
                'quantity': 3
            }
        )
        # Check that order_item3_user2 did belongs to order_user2 after the request
        self.assertTrue(order_item3_user2.exists())

        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This item for size S was added to your cart.')


class OrderSummaryViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory(username='user1')
        self.user2 = UserFactory(username='user2')

        self.size = SizeFactory()
        self.item1 = ItemFactory(price=40)
        self.item2 = ItemFactory(price=30, discount_price=20)
        self.order = OrderFactory(user=self.user1)

        OrderItemFactory(user=self.user1, item=self.item1, quantity=1, order=self.order)
        OrderItemFactory(user=self.user1, item=self.item2, quantity=1, order=self.order)

    def test_view_uses_correct_template(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:order-summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/order_summary.html')

    def test_view_returns_empty_in_context(self):
        self.client.login(username='user2', password='1234')
        response = self.client.get(reverse('core:order-summary'))

        self.assertEqual(response.context['empty'], True)

    def test_order_items_in_context(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:order-summary'))
        order_items = OrderItem.objects.filter(order=self.order, ordered=False)

        # Check that the view returns all the order items that belong to the order
        for i in range(len(order_items)):
            self.assertEqual(response.context['order_items'][i], order_items[i])

    def test_price_include_discount_in_context(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:order-summary'))

        self.assertEqual(60.0, response.context['price_include_discount'])

    def test_price_without_discount_in_context(self):
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:order-summary'))

        self.assertEqual(70.0, response.context['price_without_discount'])


class ManageOrderItemViewTest(TestCase):
    def setUp(self):
        self.user2 = User.objects.create_user(username='user2', password='1234')
        self.user1 = User.objects.create_user(username='user1', password='1234')

        self.size_s = Size.objects.create(name='S')
        self.size_m = Size.objects.create(name='M')

        self.item1 = Item.objects.create(
            name='item1', price=100, image1='img1', image2='img2', slug='item1')
        self.item2 = Item.objects.create(
            name='item2', price=100, image1='img1', image2='img2', slug='item2')
        self.item3 = Item.objects.create(
            name='item3', price=100, image1='img1', image2='img2', slug='item3')

        StockItem.objects.create(stock=0, item=self.item1, size=self.size_s)
        StockItem.objects.create(stock=25, item=self.item2, size=self.size_s)
        StockItem.objects.create(stock=5, item=self.item3, size=self.size_s)

        order_user1 = Order.objects.create(user=self.user1)
        order_user2 = Order.objects.create(user=self.user2)

        OrderItem.objects.create(
            user=self.user1, item=self.item1, size=self.size_s, quantity=5, order=order_user1
        )
        OrderItem.objects.create(
            user=self.user1, item=self.item3, size=self.size_s, quantity=1, order=order_user1
        )
        OrderItem.objects.create(
            user=self.user2, item=self.item2, size=self.size_s, quantity=20, order=order_user2
        )
        OrderItem.objects.create(
            user=self.user2, item=self.item3, size=self.size_s, quantity=20, order=order_user2
        )

    def test_view_redirects(self):
        self.client.login(username='user1', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item1.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'plus'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:order-summary'))

    def test_view_returns_404(self):
        self.client.login(username='user1', password='1234')

        # 404 page not found because of size
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item1.pk) + '/'
        response = self.client.get(url, {'size': 'X', 'op': 'plus'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context['exception'], 'No Size matches the given query.')

        # 404 page not found because of pk of item
        url = 'http://127.0.0.1:8000/manage-order-item/0/'
        response = self.client.get(url, {'size': 'S', 'op': 'plus'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context['exception'], 'No Item matches the given query.')

        # 404 page not found because order item does not exist for the given size
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item1.pk) + '/'
        response = self.client.get(url, {'size': 'M', 'op': 'plus'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.context['exception'], 'No OrderItem matches the given query.')

    def test_out_of_stock(self):
        self.client.login(username='user1', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item1.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'plus'}, follow=True)

        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This product is out of stock for this size.')

    def test_user_cannot_order_more_than_20_identical_items(self):
        self.client.login(username='user2', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item2.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'plus'}, follow=True)

        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'You cannot add more than 20 identical products to the cart.')

    def test_quantity_increased(self):
        stock_before = StockItem.objects.get(item=self.item3).stock  # The stock before the request
        # The quantity before the request
        quantity_before = OrderItem.objects.get(
            user=self.user1,
            item=self.item3,
            size=self.size_s,
            ordered=False
        ).quantity

        self.client.login(username='user1', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item3.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'plus'}, follow=True)

        stock_after = StockItem.objects.get(item=self.item3).stock  # The stock after the request
        # The quantity after the request
        quantity_after = OrderItem.objects.get(
            user=self.user1,
            item=self.item3,
            size=self.size_s,
            ordered=False
        ).quantity

        # Check that stock decreased by 1
        self.assertEqual(stock_after, stock_before - 1)
        # Check that quantity of order item increased by 1
        self.assertEqual(quantity_after, quantity_before + 1)
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This item quantity was updated.')

    def test_quantity_do_not_decreased(self):
        self.client.login(username='user1', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item3.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'minus'}, follow=True)

        quantity = OrderItem.objects.get(
            user=self.user1,
            item=self.item3,
            size=self.size_s,
            ordered=False
        ).quantity
        # Check that quantity didn't decreased because it's equal to 1
        self.assertEqual(quantity, 1)

    def test_quantity_decreased(self):
        stock_before = StockItem.objects.get(item=self.item3).stock  # The stock before the request
        # The quantity before the request
        quantity_before = OrderItem.objects.get(
            user=self.user2,
            item=self.item3,
            size=self.size_s,
            ordered=False
        ).quantity

        self.client.login(username='user2', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item3.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'minus'}, follow=True)

        stock_after = StockItem.objects.get(item=self.item3).stock  # The stock after the request
        # The quantity after the request
        quantity_after = OrderItem.objects.get(
            user=self.user2,
            item=self.item3,
            size=self.size_s,
            ordered=False
        ).quantity

        # Check that stock increased by 1
        self.assertEqual(stock_after, stock_before + 1)
        # Check that quantity of order item decreased by 1
        self.assertEqual(quantity_after, quantity_before - 1)
        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'This item quantity was updated.')

    def test_item_removed(self):
        stock_before = StockItem.objects.get(item=self.item1).stock  # The stock before the request
        order_item1_user1 = OrderItem.objects.get(
            user=self.user1,
            item=self.item1,
            ordered=False
        )

        self.client.login(username='user1', password='1234')
        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item1.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'remove'}, follow=True)

        stock_after = StockItem.objects.get(item=self.item1).stock  # The stock after the request

        self.assertEqual(stock_after, stock_before + order_item1_user1.quantity)

        # Check that the user still have the order
        order_user1 = Order.objects.filter(user=self.user1, ordered=False)
        self.assertTrue(order_user1.exists())

        url = 'http://127.0.0.1:8000/manage-order-item/' + str(self.item3.pk) + '/'
        response = self.client.get(url, {'size': 'S', 'op': 'remove'}, follow=True)
        # Now we check that the user don't have an order
        self.assertFalse(order_user1.exists())


class TestCheckoutView(TestCase):
    def setUp(self):
        self.user = UserFactory(username='user1')

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('core:checkout'))

        # Check user are redirected to login page
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/accounts/login/?next=/checkout/')

    def test_view_uses_correct_template(self):
        order = OrderFactory(user=self.user)
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/checkout.html')

    def test_error_if_no_order(self):
        """Redirect the user to the home page with an error msg if he does not have an order"""
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:checkout'), follow=True)

        message = list(response.context['messages'])
        self.assertEqual(str(message[0]), 'You do not have an active order.')
        self.assertRedirects(response, '/')

    def test_view_returns_order_in_context(self):
        order = OrderFactory(user=self.user)
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:checkout'))

        self.assertEqual(response.context['order'], order)

    def test_view_returns_form_in_context(self):
        order = OrderFactory(user=self.user)
        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:checkout'))

        self.assertTrue('form' in response.context)

    def test_view_order_items_in_context(self):
        item = ItemFactory()
        order = OrderFactory(user=self.user)
        order_item = OrderItemFactory(user=self.user, item=item, order=order)

        self.client.login(username='user1', password='1234')
        response = self.client.get(reverse('core:checkout'))

        self.assertEqual(response.context['order_items'][0], order_item)

    def test_use_default_shipping(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'payment_option': 'ST'
            }
        )
        # If the form is not valid we have a return instead of a redirect
        self.assertEqual(response.status_code, 200)

    def test_create_address(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:checkout'),
            {
                'shipping_address': 'shipping_address_1',
                'country_shipping': 'US',
                'shipping_zip': 'shipping_zip_1',
                'payment_option': 'ST'
            }
        )
        address_user = Address.objects.filter(user=self.user)
        self.assertTrue(address_user.exists())
        self.assertFalse(address_user[0].default_shipping_address)

    def test_set_default_shipping(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:checkout'),
            {
                'shipping_address': 'shipping_address_1',
                'country_shipping': 'US',
                'shipping_zip': 'shipping_zip_1',
                'set_default_shipping': True,
                'payment_option': 'ST'
            }
        )
        address_user = Address.objects.filter(user=self.user).get()
        self.assertTrue(address_user.default_shipping_address)

    def test_error_msg_if_fields_unfilled(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:checkout'),
            {
                'payment_option': 'ST'
            }
        )
        message = list(response.context['messages'])
        msg = 'Please fill in the required shipping and billing address fields.'
        self.assertEqual(str(message[0]), msg)

        response = self.client.post(
            reverse('core:checkout'),
            {
                'billing_address': 'billing_address_1',
                'country_billing': 'US',
                'billing_zip': 'billing_zip_1',
                'payment_option': 'ST'
            }
        )
        message = list(response.context['messages'])
        msg = 'Please fill in the required shipping address fields.'
        self.assertEqual(str(message[0]), msg)

    def test_use_default_billing(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:checkout'),
            {
                'shipping_address': 'shipping_address_1',
                'country_shipping': 'US',
                'shipping_zip': 'shipping_zip_1',
                'use_default_billing': True,
                'payment_option': 'ST'
            }
        )
        # If the form is not valid we have a return instead of a redirect
        self.assertEqual(response.status_code, 200)

    def test_billing_same_as_shipping_with_default_shipping(self):
        self.client.login(username='user1', password='1234')
        address = AddressFactory(user=self.user, default_shipping_address=True)
        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'billing_same_as_shipping': True,
                'payment_option': 'ST'
            }
        )
        address = Address.objects.get(user=self.user)
        self.assertEqual(address.billing_address, address.shipping_address)
        self.assertEqual(address.billing_zip, address.shipping_zip)
        self.assertFalse(address.default_billing_address)

        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'billing_same_as_shipping': True,
                'set_default_billing': True,
                'payment_option': 'ST'
            }
        )
        address = Address.objects.get(user=self.user)
        self.assertTrue(address.default_billing_address)

    def test_billing_same_as_shipping_without_default_shipping(self):
        self.client.login(username='user1', password='1234')
        response = self.client.post(
            reverse('core:checkout'),
            {
                'shipping_address': 'shipping_address_1',
                'country_shipping': 'US',
                'shipping_zip': 'shipping_zip_1',
                'billing_same_as_shipping': True,
                'payment_option': 'ST'
            }
        )
        address = Address.objects.get(user=self.user)
        self.assertEqual(address.billing_address, address.shipping_address)
        self.assertEqual(address.billing_zip, address.shipping_zip)
        self.assertFalse(address.default_billing_address)

        response = self.client.post(
            reverse('core:checkout'),
            {
                'shipping_address': 'shipping_address_1',
                'country_shipping': 'US',
                'shipping_zip': 'shipping_zip_1',
                'billing_same_as_shipping': True,
                'set_default_billing': True,
                'payment_option': 'ST'
            }
        )
        address = Address.objects.get(user=self.user)
        self.assertTrue(address.default_billing_address)

    def test_billing_address(self):
        self.client.login(username='user1', password='1234')
        address = AddressFactory(user=self.user, default_shipping_address=True)
        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'billing_address': 'billing_address_1',
                'country_billing': 'US',
                'billing_zip': 'billing_zip_1',
                'payment_option': 'ST'
            }
        )
        address = Address.objects.get(user=self.user)
        self.assertEqual(address.billing_address, 'billing_address_1')
        self.assertEqual(address.billing_zip, 'billing_zip_1')
        self.assertFalse(address.default_billing_address)

    def test_billing_address_with_set_default_billing(self):
        self.client.login(username='user1', password='1234')
        address = AddressFactory(user=self.user, default_shipping_address=True)
        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'billing_address': 'billing_address_1',
                'country_billing': 'US',
                'billing_zip': 'billing_zip_1',
                'set_default_billing': True,
                'payment_option': 'ST'
            }
        )
        address = Address.objects.get(user=self.user)
        self.assertEqual(address.billing_address, 'billing_address_1')
        self.assertEqual(address.billing_zip, 'billing_zip_1')
        self.assertTrue(address.default_billing_address)

    def test_error_msg_if_not_billing_address(self):
        self.client.login(username='user1', password='1234')
        address = AddressFactory(user=self.user, default_shipping_address=True)
        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'payment_option': 'ST'
            }
        )
        message = list(response.context['messages'])
        msg = 'Please fill in the required billing address fields.'
        self.assertEqual(str(message[0]), msg)

    def test_redirect_if_form_valid(self):
        self.client.login(username='user1', password='1234')
        address = AddressFactory(user=self.user, default_shipping_address=True)
        OrderFactory(user=self.user)
        response = self.client.post(
            reverse('core:checkout'),
            {
                'use_default_shipping': True,
                'billing_address': 'billing_address_1',
                'country_billing': 'US',
                'billing_zip': 'billing_zip_1',
                'payment_option': 'ST'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/payment/create-payment/')
