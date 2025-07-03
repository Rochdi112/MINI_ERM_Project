from django.test import TestCase, Client
from .models import Materiel
from django.urls import reverse

class MaterielModelTest(TestCase):
    def test_str(self):
        m = Materiel.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        self.assertIn('M', str(m))

class MaterielCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(self.create_user())
        self.obj = Materiel.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
    def create_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user('user', 'user@test.com', 'pass')
    def test_list(self):
        resp = self.client.get(reverse('app_materiels:materiel_list'))
        self.assertEqual(resp.status_code, 200)
    def test_create(self):
        resp = self.client.post(reverse('app_materiels:materiel_create'), {'nom': 'Nouveau', 'reference': 'R', 'marque': 'M', 'date_installation': '2024-01-01'})
        self.assertEqual(Materiel.objects.count(), 2)
    def test_update(self):
        resp = self.client.post(reverse('app_materiels:materiel_update', args=[self.obj.pk]), {'nom': 'Modif', 'reference': 'R', 'marque': 'M', 'date_installation': '2024-01-01'})
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.nom, 'Modif')
    def test_delete(self):
        resp = self.client.post(reverse('app_materiels:materiel_delete', args=[self.obj.pk]))
        self.assertEqual(Materiel.objects.count(), 0)
