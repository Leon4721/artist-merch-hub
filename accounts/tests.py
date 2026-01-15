from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
    
    def test_profile_auto_created(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertFalse(self.user.profile.has_paid)


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_signup_loads(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_loads(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_logged_in_redirects_from_signup(self):
        User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 302)