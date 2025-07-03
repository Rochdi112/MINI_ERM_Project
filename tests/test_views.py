from django.test import TestCase, Client
from django.urls import reverse
from app_clients.models import Client as ClientModel
from app_techniciens.models import Technicien
from app_interventions.models import Intervention

class BasicViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_test = ClientModel.objects.create(nom="Client Test", adresse="Casablanca", contact="0661000000")
        self.technicien_test = Technicien.objects.create(nom="Technicien Test", specialite="HVAC")

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_clients_list_view(self):
        response = self.client.get("/clients/")
        self.assertEqual(response.status_code, 200)

    def test_techniciens_list_view(self):
        response = self.client.get("/techniciens/")
        self.assertEqual(response.status_code, 200)

    def test_interventions_list_view(self):
        response = self.client.get("/interventions/")
        self.assertEqual(response.status_code, 200)
