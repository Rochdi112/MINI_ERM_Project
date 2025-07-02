from django.db import models
from app_techniciens.models import Technicien
from app_clients.models import Client
from app_materiels.models import Materiel

class Intervention(models.Model):
    TYPE_CHOICES = [
        ('corrective', 'Corrective'),
        ('preventive', 'Préventive'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    technicien = models.ForeignKey(Technicien, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateField(auto_now_add=True)
    date_cloture = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.type} - {self.client.nom} ({self.statut})"
