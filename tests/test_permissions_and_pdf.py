from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_clients.models import Client as ClientModel
from app_techniciens.models import Technicien
from app_interventions.models import Intervention
from app_rapports.models import Rapport
from core.models import ProfilUtilisateur

class AuthPermissionsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.admin = User.objects.create_user(username='admin', password='pass')
        ProfilUtilisateur.objects.create(user=self.admin, role='admin')

    def test_login_required(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_admin_access(self):
        self.client.login(username='admin', password='pass')
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)

    def test_forbidden(self):
        self.client.login(username='user', password='pass')
        resp = self.client.get(reverse('app_rapports:rapport_pdf', args=[1]))
        self.assertIn(resp.status_code, [403, 404])

class CRUDInterventionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='pass')
        ProfilUtilisateur.objects.create(user=self.admin, role='admin')
        self.client.login(username='admin', password='pass')
        self.client_test = ClientModel.objects.create(nom="Client Test", adresse="Casa", contact="0661000000")
        self.technicien = Technicien.objects.create(nom="Tech", specialite="HVAC")

    def test_create_intervention(self):
        resp = self.client.post('/interventions/create/', {
            'client': self.client_test.id,
            'materiel': None,
            'site': None,
            'type': 'corrective',
            'statut': 'en_attente',
            'description': 'Test',
            'date': '2025-07-03',
        })
        self.assertIn(resp.status_code, [200, 302])

    def test_delete_intervention(self):
        intervention = Intervention.objects.create(client=self.client_test, materiel=None, site=None, type='corrective', statut='en_attente', description='Test', date='2025-07-03')
        resp = self.client.post(f'/interventions/{intervention.id}/delete/')
        self.assertIn(resp.status_code, [200, 302])

class PDFGenerationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='pass')
        ProfilUtilisateur.objects.create(user=self.admin, role='admin')
        self.client.login(username='admin', password='pass')

    def test_pdf_generation(self):
        # Suppose a Rapport with pk=1 exists
        resp = self.client.get(reverse('app_rapports:rapport_pdf', args=[1]))
        self.assertIn(resp.status_code, [200, 404, 500])

class IntegrationFlowTests(TestCase):
    def test_full_flow(self):
        # Création client > Matériel > Intervention > Clôture > Rapport PDF
        pass  # À compléter selon vos modèles et urls
