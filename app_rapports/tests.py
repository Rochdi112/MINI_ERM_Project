from django.test import TestCase, Client
from .models import Rapport
from django.urls import reverse
from django.contrib.auth.models import User
from app_interventions.models import Intervention
from app_clients.models import Client as C
from app_materiels.models import Materiel as M
from app_techniciens.models import Technicien as T

class RapportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        c = C.objects.create(nom='C', adresse='A', contact='C')
        m = M.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        t = T.objects.create(nom='T', email='t@t.com', specialite='S')
        self.intervention = Intervention.objects.create(client=c, materiel=m, type='corrective', statut='en_cours', description='desc')
        self.intervention.techniciens.add(t)
        self.rapport = Rapport.objects.create(intervention=self.intervention, contenu='Contenu')
    def test_str(self):
        r = self.rapport
        self.assertIn('Rapport', str(r))

class RapportPDFTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('user', 'u@u.com', 'pass')
        # Créer ou récupérer un profil utilisateur admin pour l'utilisateur
        from core.models import ProfilUtilisateur
        ProfilUtilisateur.objects.get_or_create(user=user, defaults={'role': 'admin'})
        self.client.force_login(user)
        c = C.objects.create(nom='C', adresse='A', contact='C')
        m = M.objects.create(nom='M', reference='R', marque='Marque', date_installation='2024-01-01')
        t = T.objects.create(nom='T', email='t@t.com', specialite='S')
        self.i = Intervention.objects.create(client=c, materiel=m, type='corrective', statut='en_cours', description='desc')
        self.i.techniciens.add(t)
        self.r = Rapport.objects.create(intervention=self.i, contenu='Contenu')
    def test_pdf(self):
        resp = self.client.get(reverse('app_rapports:generate_pdf', args=[self.r.pk]))
        self.assertIn(resp.status_code, [200, 302])
