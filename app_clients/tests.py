from django.test import TestCase, Client
from .models import Client
from django.urls import reverse

class ClientModelTest(TestCase):
    def test_str(self):
        c = Client.objects.create(nom='Test', adresse='Adresse', contact='Contact')
        self.assertEqual(str(c), 'Test')

class ClientCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(self.create_user())
        self.obj = Client.objects.create(nom='Test', adresse='Adresse', contact='Contact')
    def create_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user('user', 'user@test.com', 'pass')
    def test_list(self):
        resp = self.client.get(reverse('app_clients:client_list'))
        self.assertEqual(resp.status_code, 200)
    def test_create(self):
        resp = self.client.post(reverse('app_clients:client_create'), {'nom': 'Nouveau', 'adresse': 'A', 'contact': 'C'})
        self.assertEqual(Client.objects.count(), 2)
    def test_update(self):
        resp = self.client.post(reverse('app_clients:client_update', args=[self.obj.pk]), {'nom': 'Modif', 'adresse': 'A', 'contact': 'C'})
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.nom, 'Modif')
    def test_delete(self):
        resp = self.client.post(reverse('app_clients:client_delete', args=[self.obj.pk]))
        self.assertEqual(Client.objects.count(), 0)
