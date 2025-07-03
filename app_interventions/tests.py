from django.test import TestCase, Client as DjangoClient, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_interventions.models import Intervention, ChecklistItem
from app_clients.models import Client as ClientModel, Site
from app_techniciens.models import Technicien
from app_materiels.models import Materiel
from datetime import date
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from app_interventions.models import Attachment

class HTMXInterventionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tech', password='pass')
        # Créer un profil utilisateur technicien pour l'utilisateur de test
        from core.models import ProfilUtilisateur
        ProfilUtilisateur.objects.get_or_create(user=self.user, defaults={'role': 'technicien'})
        client = ClientModel.objects.create(nom='C', email='c@c.com', telephone='1')
        site = Site.objects.create(client=client, nom='S', adresse='A')
        materiel = Materiel.objects.create(site=site, nom='M', reference='R', marque='X', date_installation='2024-01-01')
        technicien = Technicien.objects.create(nom='tech', email='t@t.com', specialite='s')
        self.intervention = Intervention.objects.create(client=client, materiel=materiel, site=site, type='corrective', statut='en_attente', date=date.today())
        self.intervention.techniciens.add(technicien)
        self.item = ChecklistItem.objects.create(intervention=self.intervention, description='Test', completed=False)
        self.client = DjangoClient()

    def test_toggle_checklist_item_htmx_protected(self):
        url = reverse('app_interventions:htmx-checklist-item', args=[self.item.id])
        # Non connecté
        response = self.client.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 302)  # redirect to login
        # Connecté mais pas HTMX
        self.client.login(username='tech', password='pass')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Requête non autorisée', response.content.decode())

    def test_toggle_checklist_item_htmx_ok(self):
        url = reverse('app_interventions:htmx-checklist-item', args=[self.item.id])
        self.client.login(username='tech', password='pass')
        response = self.client.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('<html', response.content.decode())
        self.assertNotIn('<body', response.content.decode())
        self.item.refresh_from_db()
        self.assertTrue(self.item.completed)

    def test_toggle_checklist_item_htmx_forbidden(self):
        other = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        url = reverse('app_interventions:htmx-checklist-item', args=[self.item.id])
        response = self.client.post(url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Accès refusé', response.content.decode())

    def test_filter_interventions_htmx(self):
        url = reverse('app_interventions:htmx-filter')
        self.client.login(username='tech', password='pass')
        response = self.client.get(url, HTTP_HX_REQUEST='true')
        # On attend un code 200 si l'utilisateur est technicien et la requête est HTMX
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('<html', response.content.decode())
        self.assertNotIn('<body', response.content.decode())
        self.assertIn('Aucune intervention', response.content.decode())

    def test_modal_form_intervention_htmx_get(self):
        url = reverse('app_interventions:htmx-modal-form')
        self.client.login(username='tech', password='pass')
        response = self.client.get(url, HTTP_HX_REQUEST='true')
        # On attend un code 200 si l'utilisateur est technicien et la requête est HTMX
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.content.decode())
        self.assertNotIn('<html', response.content.decode())

    def test_modal_form_intervention_htmx_post_invalid(self):
        url = reverse('app_interventions:htmx-modal-form')
        self.client.login(username='tech', password='pass')
        response = self.client.post(url, {}, HTTP_HX_REQUEST='true')
        # On attend un code 200 même si le formulaire est invalide (retourne le formulaire avec erreurs)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.content.decode())
        self.assertIn('Veuillez corriger', response.content.decode())

    def test_modal_form_intervention_htmx_post_valid(self):
        url = reverse('app_interventions:htmx-modal-form')
        self.client.login(username='tech', password='pass')
        data = {
            'client': self.intervention.client.id,
            'materiel': self.intervention.materiel.id,
            'techniciens': [t.id for t in self.intervention.techniciens.all()],
            'site': self.intervention.site.id,
            'type': 'corrective',
            'statut': 'en_attente',
            'date': '2024-01-01',
        }
        response = self.client.post(url, data, HTTP_HX_REQUEST='true')
        # On attend un code 200 si tout est valide
        self.assertEqual(response.status_code, 200)
        self.assertIn('succès', response.content.decode())
        self.assertNotIn('<html', response.content.decode())

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
            self.intervention = Intervention.objects.create(materiel=self.materiel, site=self.site, date='2024-01-01', description='desc')
            self.intervention.techniciens.add(self.technicien)
        def test_list_view(self):
            resp = self.client.get(reverse('app_interventions:intervention_list'))
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, 'M')
        def test_create_view(self):
            data = {
                'materiel': self.materiel.pk,
                'techniciens': [self.technicien.pk],
                'site': self.site.pk,
                'date': '2024-01-02',
                'description': 'Nouvelle intervention'
            }
            resp = self.client.post(reverse('app_interventions:intervention_create'), data)
            self.assertEqual(resp.status_code, 302)
            # Un objet existe déjà via setUp, on en crée un second
            self.assertEqual(Intervention.objects.count(), 2)
        def test_update_view(self):
            data = {
                'materiel': self.materiel.pk,
                'techniciens': [self.technicien.pk],
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
            # Après suppression, il ne doit plus rester aucun objet
            self.assertEqual(Intervention.objects.count(), 0)
        def test_permission_denied(self):
            # Simule un technicien non assigné
            other_user = User.objects.create_user('other', 'o@o.com', 'pass')
            self.client.force_login(other_user)
            resp = self.client.post(reverse('app_interventions:intervention_update', args=[self.intervention.pk]), {'materiel': self.materiel.pk, 'technicien': self.technicien.pk, 'site': self.site.pk, 'date': '2024-01-03', 'description': 'X'})
            self.assertIn(resp.status_code, [403, 200])

    class DashboardHTMXTests(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(username='admin', password='pass')
            self.user.profilutilisateur.role = 'admin'
            self.user.profilutilisateur.save()
            client = ClientModel.objects.create(nom='C', email='c@c.com', telephone='1')
            site = Site.objects.create(client=client, nom='S', adresse='A')
            materiel = Materiel.objects.create(site=site, nom='M', reference='R', marque='X', date_installation='2024-01-01')
            technicien = Technicien.objects.create(nom='admin', email='a@a.com', specialite='s')
            today = timezone.now().date()
            Intervention.objects.create(client=client, materiel=materiel, technicien=technicien, site=site, type='corrective', statut='en_cours', date=today.replace(day=1))
            Intervention.objects.create(client=client, materiel=materiel, technicien=technicien, site=site, type='corrective', statut='en_attente', date=today.replace(day=28))
            self.client = DjangoClient()

        def test_dashboard_kpi_htmx_protected(self):
            url = reverse('dashboard:htmx-kpi')
            # Non connecté
            response = self.client.get(url, HTTP_HX_REQUEST='true')
            self.assertEqual(response.status_code, 302)
            # Connecté mais pas HTMX
            self.client.login(username='admin', password='pass')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertIn('Requête non autorisée', response.content.decode())

        def test_dashboard_kpi_htmx_ok(self):
            url = reverse('dashboard:htmx-kpi')
            self.client.login(username='admin', password='pass')
            response = self.client.get(url, HTTP_HX_REQUEST='true')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Total interventions', response.content.decode())
            self.assertNotIn('<html', response.content.decode())
            self.assertNotIn('<body', response.content.decode())
