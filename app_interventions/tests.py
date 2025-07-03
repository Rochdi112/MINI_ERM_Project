from django.test import TestCase, Client
from .models import Intervention, ChecklistItem, Attachment
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

class InterventionModelTest(TestCase):
    def test_str(self):
        from app_clients.models import Client as C
        from app_materiels.models import Materiel as M
        from app_techniciens.models import Technicien as T
        c = C.objects.create(nom='C', adresse='A', contact='C')
        m = M.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        t = T.objects.create(nom='T', email='t@t.com', specialite='S')
        i = Intervention.objects.create(client=c, materiel=m, technicien=t, type='corrective', statut='en_cours', description='desc')
        self.assertIn('corrective', str(i))

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
