from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass')
    
    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            stripe_session_id="test_123",
            amount=9.99,
            currency="gbp"
        )
        self.assertEqual(float(order.amount), 9.99)


class CheckoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_checkout_requires_login(self):
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 302)