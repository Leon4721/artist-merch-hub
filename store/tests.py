from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Product, Review


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Track",
            description="Test description",
            price=9.99,
            product_type="digital"
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.title, "Test Track")
        self.assertEqual(float(self.product.price), 9.99)
    
    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Track")


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(title="Track 1", price=5.99)
    
    def test_product_list_loads(self):
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Track 1")
    
    def test_search_works(self):
        response = self.client.get('/store/?q=Track')
        self.assertContains(response, "Track 1")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.product = Product.objects.create(title="Product", price=10)
    
    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Great!"
        )
        self.assertEqual(review.rating, 5)