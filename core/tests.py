from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user', 'u@u.com', 'pass')
        self.client.force_login(self.user)

    def test_dashboard(self):
        resp = self.client.get(reverse('dashboard:dashboard'))  # Correction du nom de la route
        self.assertEqual(resp.status_code, 200)
