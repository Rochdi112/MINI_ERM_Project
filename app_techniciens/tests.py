from django.test import TestCase, Client
from .models import Technicien
from django.urls import reverse

class TechnicienModelTest(TestCase):
    def test_str(self):
        t = Technicien.objects.create(nom='Tech', email='t@t.com', specialite='Spec')
        self.assertIn('Tech', str(t))

class TechnicienCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(self.create_user())
        self.obj = Technicien.objects.create(nom='Tech', email='t@t.com', specialite='Spec')
    def create_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user('user', 'user@test.com', 'pass')
    def test_list(self):
        resp = self.client.get(reverse('app_techniciens:technicien_list'))
        self.assertEqual(resp.status_code, 200)
    def test_create(self):
        resp = self.client.post(reverse('app_techniciens:technicien_create'), {'nom': 'Nouveau', 'email': 'n@n.com', 'specialite': 'S'})
        self.assertEqual(Technicien.objects.count(), 2)
    def test_update(self):
        resp = self.client.post(reverse('app_techniciens:technicien_update', args=[self.obj.pk]), {'nom': 'Modif', 'email': 't@t.com', 'specialite': 'S'})
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.nom, 'Modif')
    def test_delete(self):
        resp = self.client.post(reverse('app_techniciens:technicien_delete', args=[self.obj.pk]))
        self.assertEqual(Technicien.objects.count(), 0)
