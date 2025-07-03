from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Intervention, ChecklistItem, Attachment
from app_materiels.models import Materiel
from app_techniciens.models import Technicien
from app_clients.models import Site, Client as ClientModel

class InterventionModelTest(TestCase):
    def test_str(self):
        c = ClientModel.objects.create(nom='C', email='c@c.com', telephone='123')
        s = Site.objects.create(client=c, nom='Site1', adresse='Adr')
        m = Materiel.objects.create(site=s, nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        t = Technicien.objects.create(nom='T', email='t@t.com', specialite='S')
        i = Intervention.objects.create(materiel=m, technicien=t, site=s, date='2024-01-01', description='desc')
        self.assertIn('M', str(i))

class ChecklistTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(User.objects.create_user('user', 'u@u.com', 'pass'))
        from app_clients.models import Client as C
        from app_materiels.models import Materiel as M
        from app_techniciens.models import Technicien as T
        self.c = C.objects.create(nom='C', adresse='A', contact='C')
        self.m = M.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        self.t = T.objects.create(nom='T', email='t@t.com', specialite='S')
        self.i = Intervention.objects.create(client=self.c, materiel=self.m, technicien=self.t, type='corrective', statut='en_cours', description='desc')
        self.item = ChecklistItem.objects.create(intervention=self.i, description='Check', completed=False)
    def test_checklist_update(self):
        resp = self.client.post(reverse('app_interventions:checklist_item_update', args=[self.item.pk]), {'description': 'Check', 'completed': True})
        self.item.refresh_from_db()
        self.assertTrue(self.item.completed)

class AttachmentUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.force_login(User.objects.create_user('user', 'u@u.com', 'pass'))
        from app_clients.models import Client as C
        from app_materiels.models import Materiel as M
        from app_techniciens.models import Technicien as T
        self.c = C.objects.create(nom='C', adresse='A', contact='C')
        self.m = M.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        self.t = T.objects.create(nom='T', email='t@t.com', specialite='S')
        self.i = Intervention.objects.create(client=self.c, materiel=self.m, technicien=self.t, type='corrective', statut='en_cours', description='desc')
    def test_upload(self):
        file = SimpleUploadedFile('test.pdf', b'filecontent', content_type='application/pdf')
        resp = self.client.post(reverse('app_interventions:htmx_upload_attachment', args=[self.i.pk]), {'file': file})
        self.assertEqual(Attachment.objects.count(), 1)

class InterventionCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user', 'u@u.com', 'pass')
        self.client.force_login(self.user)
        c = ClientModel.objects.create(nom='C', email='c@c.com', telephone='123')
        self.site = Site.objects.create(client=c, nom='Site1', adresse='Adr')
        self.materiel = Materiel.objects.create(site=self.site, nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        self.technicien = Technicien.objects.create(nom='T', email='t@t.com', specialite='S')
        self.intervention = Intervention.objects.create(materiel=self.materiel, technicien=self.technicien, site=self.site, date='2024-01-01', description='desc')
    def test_list_view(self):
        resp = self.client.get(reverse('app_interventions:intervention_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'M')
    def test_create_view(self):
        data = {
            'materiel': self.materiel.pk,
            'technicien': self.technicien.pk,
            'site': self.site.pk,
            'date': '2024-01-02',
            'description': 'Nouvelle intervention'
        }
        resp = self.client.post(reverse('app_interventions:intervention_create'), data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Intervention.objects.count(), 2)
    def test_update_view(self):
        data = {
            'materiel': self.materiel.pk,
            'technicien': self.technicien.pk,
            'site': self.site.pk,
            'date': '2024-01-03',
            'description': 'Modif'
        }
        resp = self.client.post(reverse('app_interventions:intervention_update', args=[self.intervention.pk]), data)
        self.assertEqual(resp.status_code, 302)
        self.intervention.refresh_from_db()
        self.assertEqual(self.intervention.description, 'Modif')
    def test_delete_view(self):
        resp = self.client.post(reverse('app_interventions:intervention_delete', args=[self.intervention.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Intervention.objects.count(), 0)
    def test_permission_denied(self):
        # Simule un technicien non assigné
        other_user = User.objects.create_user('other', 'o@o.com', 'pass')
        self.client.force_login(other_user)
        resp = self.client.post(reverse('app_interventions:intervention_update', args=[self.intervention.pk]), {'materiel': self.materiel.pk, 'technicien': self.technicien.pk, 'site': self.site.pk, 'date': '2024-01-03', 'description': 'X'})
        self.assertIn(resp.status_code, [403, 200])
