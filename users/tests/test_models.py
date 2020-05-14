from django.test import TestCase
from users.tests.factories import AddressFactory, UserFactory


class AddressModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_factory(self):
        address_factory = AddressFactory(user=self.user)

        self.assertIsNotNone(address_factory)
        self.assertNotEqual('', address_factory.shipping_address)
        self.assertNotEqual('', address_factory.billing_address)
        self.assertNotEqual('', address_factory.shipping_zip)
        self.assertNotEqual('', address_factory.billing_zip)

    def test_has_user(self):
        address_factory = AddressFactory(user=self.user)

        self.assertEqual(self.user, address_factory.user)

    def test_shipping_address(self):
        shipping_address = 'shipping address'
        address_factory = AddressFactory(user=self.user, shipping_address=shipping_address)

        self.assertEqual(shipping_address, address_factory.shipping_address)

    def test_billing_address(self):
        billing_address = 'billing address'
        address_factory = AddressFactory(user=self.user, billing_address=billing_address)

        self.assertEqual(billing_address, address_factory.billing_address)

    def test_has_shipping_zip(self):
        shipping_zip = 'shipping_zip_1'
        address_factory = AddressFactory(user=self.user, shipping_zip=shipping_zip)

        self.assertEqual(shipping_zip, address_factory.shipping_zip)

    def test_has_billing_zip(self):
        billing_zip = 'billing_zip_1'
        address_factory = AddressFactory(user=self.user, billing_zip=billing_zip)

        self.assertEqual(billing_zip, address_factory.billing_zip)

    def test_str(self):
        address_factory = AddressFactory(user=self.user)
        user = str(self.user)

        self.assertEqual(f'Address of user {user}', str(address_factory))