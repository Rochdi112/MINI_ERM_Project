from django.db import models
from django.utils import timezone
from app_techniciens.models import Technicien
from app_clients.models import Client, Site
from app_materiels.models import Materiel
from django.contrib.auth.models import User

class Intervention(models.Model):
    TYPE_CHOICES = [
        ('corrective', 'Corrective'),
        ('preventive', 'Préventive'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="interventions", verbose_name="Client")
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE, related_name="interventions", verbose_name="Matériel")
    techniciens = models.ManyToManyField(Technicien, related_name="interventions", verbose_name="Techniciens")
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1, verbose_name="Site")  # Ajout d'un site par défaut pour migration
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateField(auto_now_add=True, verbose_name="Date de création")
    date_cloture = models.DateField(null=True, blank=True, verbose_name="Date de clôture")
    description = models.TextField(blank=True, verbose_name="Description")
    date = models.DateField(default=timezone.now, verbose_name="Date d'intervention")
    signature_path = models.ImageField(upload_to='signatures/', null=True, blank=True, verbose_name="Signature")

    class Meta:
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"

    def __str__(self):
        return f"{self.materiel.nom} - {self.site.nom} ({self.date})"

class ChecklistItem(models.Model):
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='checklist_items', verbose_name="Intervention")
    description = models.CharField(max_length=255, verbose_name="Description")
    completed = models.BooleanField(default=False, verbose_name="Terminé")

    def __str__(self):
        return f"{self.description} ({'✔' if self.completed else '✗'})"

class FichierJoint(models.Model):
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='fichiers_joints', verbose_name="Intervention")
    fichier = models.FileField(upload_to='fichiers_joints/', verbose_name="Fichier")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")

    def __str__(self):
        return f"Fichier pour intervention {self.intervention.id}"

class Attachment(models.Model):
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE, related_name='attachments', verbose_name="Intervention")
    file = models.FileField(upload_to='attachments/', verbose_name="Fichier")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ajouté par")

    def __str__(self):
        return f"Fichier pour intervention {self.intervention.id}"
