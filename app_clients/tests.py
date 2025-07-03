from django.test import TestCase, Client
from .models import Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_interventions.models import ChecklistItem, Intervention

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        # Création des objets liés obligatoires
        client = Client.objects.create(nom='Test', adresse='Adresse', contact='Contact')
        from app_clients.models import Site
        from app_materiels.models import Materiel
        from app_techniciens.models import Technicien
        site = Site.objects.create(client=client, nom='SiteTest', adresse='Adresse site')
        materiel = Materiel.objects.create(site=site, nom='MatérielTest', reference='REF', marque='Marque', date_installation='2024-01-01')
        technicien = Technicien.objects.create(nom='TechTest', email='tech@test.com', specialite='Spec')
        intervention = Intervention.objects.create(
            client=client,
            materiel=materiel,
            site=site,
            type='corrective',
            statut='en_attente',
            date='2024-01-01'
        )
        intervention.techniciens.add(technicien)
        self.client_obj = intervention.client
        self.item = ChecklistItem.objects.create(description='test item', completed=False, intervention=intervention)
    def test_str(self):
        c = self.client_obj
        self.assertEqual(str(c), 'Test')

class ClientCRUDTest(TestCase):
    def setUp(self):
        # Utiliser le client de test Django sans masquer le modèle Client
        from django.test import Client as DjangoClient
        self.client = DjangoClient()
        self.user = User.objects.create_user('user', 'user@test.com', 'pass')
        self.client.force_login(self.user)
        self.obj = Client.objects.create(nom='Test', adresse='Adresse', contact='Contact')
    def test_list(self):
        resp = self.client.get(reverse('app_clients:client_list'))
        self.assertEqual(resp.status_code, 200)
    def test_create(self):
        # Un client par défaut + celui du setUp + celui créé ici
        resp = self.client.post(reverse('app_clients:client_create'), {'nom': 'Nouveau', 'adresse': 'A', 'contact': 'C'})
        self.assertEqual(Client.objects.count(), 3)
    def test_update(self):
        resp = self.client.post(reverse('app_clients:client_update', args=[self.obj.pk]), {'nom': 'Modif', 'adresse': 'A', 'contact': 'C'})
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.nom, 'Modif')
    def test_delete(self):
        # Après suppression, il doit rester le client par défaut
        resp = self.client.post(reverse('app_clients:client_delete', args=[self.obj.pk]))
        self.assertEqual(Client.objects.count(), 1)
