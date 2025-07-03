from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(User.objects.create_user('user', 'u@u.com', 'pass'))
    def test_dashboard(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
