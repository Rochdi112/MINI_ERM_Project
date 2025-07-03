from django.test import TestCase, Client
from .models import Materiel
from django.urls import reverse
from django.contrib.auth.models import User
from app_clients.models import Site  # Ajout import Site

class MaterielModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.site = Site.objects.create(nom='S', client_id=1, adresse='A')  # Création d'un site par défaut
        self.materiel = Materiel.objects.create(site=self.site, nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        
    def test_str(self):
        m = self.materiel
        self.assertIn('M', str(m))

class MaterielCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(self.create_user())
        self.site = Site.objects.create(nom='S', client_id=1, adresse='A')  # Création d'un site par défaut
        self.obj = Materiel.objects.create(site=self.site, nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
    def create_user(self):
        from django.contrib.auth.models import User
        return User.objects.create_user('user', 'user@test.com', 'pass')
    def test_list(self):
        resp = self.client.get(reverse('app_materiels:materiel_list'))
        self.assertEqual(resp.status_code, 200)
    def test_create(self):
        # Un objet existe déjà via setUp, on en crée un second
        resp = self.client.post(reverse('app_materiels:materiel_create'), {'site': self.site.id, 'nom': 'Nouveau', 'reference': 'R', 'marque': 'M', 'date_installation': '2024-01-01'})
        self.assertEqual(Materiel.objects.count(), 2)
    def test_update(self):
        resp = self.client.post(reverse('app_materiels:materiel_update', args=[self.obj.pk]), {'site': self.site.id, 'nom': 'Modif', 'reference': 'R', 'marque': 'M', 'date_installation': '2024-01-01'})
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.nom, 'Modif')
    def test_delete(self):
        # Après suppression, il ne doit plus rester aucun objet
        resp = self.client.post(reverse('app_materiels:materiel_delete', args=[self.obj.pk]))
        self.assertEqual(Materiel.objects.count(), 0)
