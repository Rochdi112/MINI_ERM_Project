from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_interventions.models import Intervention, ChecklistItem
from app_clients.models import Client as ClientModel, Site
from app_techniciens.models import Technicien
from app_materiels.models import Materiel

class HTMXChecklistTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tech', password='pass')
        self.user.profilutilisateur.role = 'technicien'
        self.user.profilutilisateur.save()
        client = ClientModel.objects.create(nom='C', email='c@c.com', telephone='1')
        site = Site.objects.create(client=client, nom='S', adresse='A')
        materiel = Materiel.objects.create(site=site, nom='M', reference='R', marque='X', date_installation='2024-01-01')
        technicien = Technicien.objects.create(nom='tech', email='t@t.com', specialite='s')
        self.intervention = Intervention.objects.create(client=client, materiel=materiel, technicien=technicien, site=site, type='corrective', statut='en_attente', date='2024-01-01')
        self.item = ChecklistItem.objects.create(intervention=self.intervention, description='Test', completed=False)
        self.client = Client()

    def test_htmx_checklist_toggle_protected(self):
        url = reverse('app_interventions:htmx_checklist_toggle', args=[self.item.id])
        # Non connecté
        response = self.client.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 302)  # redirect to login
        # Connecté mais pas HTMX
        self.client.login(username='tech', password='pass')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_htmx_checklist_toggle_ok(self):
        url = reverse('app_interventions:htmx_checklist_toggle', args=[self.item.id])
        self.client.login(username='tech', password='pass')
        response = self.client.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertIn('checklist-item-', response.content.decode())
        self.item.refresh_from_db()
        self.assertTrue(self.item.completed)

    def test_htmx_checklist_toggle_forbidden(self):
        # Un autre utilisateur ne peut pas toggle
        other = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        url = reverse('app_interventions:htmx_checklist_toggle', args=[self.item.id])
        response = self.client.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Accès refusé', response.content.decode())
